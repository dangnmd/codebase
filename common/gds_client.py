import time
import json
import xml.etree.ElementTree as ET
import redis
from .logger import log
from .kafka_client import KafkaConsumer, RdKafkaConsumer
from kazoo.client import KazooClient


class GdsClientError(Exception):
	def __init__(self, value):
		super(GdsClientError, self).__init__(value)
		self.value = value

	def __str__(self):
		return repr(self.value)


class GdsRecord:
	COMMAND_DELETE = 0
	COMMAND_INSERT = 1
	COMMAND_UPDATE = 2
	COMMAND_STR_MAP = {
		'delete': COMMAND_DELETE,
		'insert': COMMAND_INSERT,
		'update': COMMAND_UPDATE,
	}

	def __init__(self, command, table, timestamp, field_num, new_row, old_row):
		"""
		Parameters
		----------
		command : enum
			gds record command type
		table : string
			table name, the format is "database.table_name"
		timestamp : int
			timestamp, seconds since 1970
		field_num : int
			fields number of this table
		new_row: array
			every elements in this array is string or None
		old_row: array
			every elements in this array is string or None
		"""
		self.command = command
		self.table = table
		self.timestamp = timestamp
		self.field_num = field_num
		self.new_row = new_row
		self.old_row = old_row

	def __str__(self):
		v = {
			'command': self.command,
			'table': self.table,
			'timestamp': self.timestamp,
			'field_num': self.field_num,
			'new_row': self.new_row,
			'old_row': self.old_row
		}
		return str(v)

	@staticmethod
	def parse_row(table_name, origin_row):
		if origin_row is None:
			return None

		new_row = {}
		for k in list(origin_row.keys()):
			v = origin_row[k]
			new_row[int(k)] = v
		return new_row

	@staticmethod
	def parse_from(v, row_parser=None):
		try:
			v = json.loads(v)
			command = v['command']
			command = GdsRecord.COMMAND_STR_MAP.get(command)

			table = v['table']
			timestamp = v['timestamp']
			field_num = v['fieldnum']
			new_row = v.get('newrow')
			old_row = v.get('oldrow')
			if row_parser is not None:
				new_row = row_parser(table, new_row)
				old_row = row_parser(table, old_row)

			record = GdsRecord(command, table, timestamp, field_num, new_row, old_row)
			return record
		except:
			return None


class GdsBaseClient(object):
	def __init__(self, zk_addrs, znode):
		self._id = znode
		self._zk = KazooClient(hosts=zk_addrs, read_only=True)
		self._zk.start()
		self._config, _ = self._zk.get(znode + '/config')


class GdsRedisClient(GdsBaseClient):
	DATE_KEY = "datelist"
	SEQ_KEY_FORMAT = "s.%s"
	VAL_KEY_FORMAT = "v.%s.%d"
	MAX_DATE = 99999999
	RETRY_TIMES = 2

	def __init__(self, zk_addrs, znode, offset=None):
		"""
		Parameters
		----------
		zk_addrs : string
		  Zookeeper hosts. Example: "10.232.98.31:2181,10.232.98.32:3181"
		znode : string
		  Zookeeper znode. Example: "/gds/test_db"
		offset : string
		  Redis read offset. If offset is None, read from latest record
		"""
		try:
			super(GdsRedisClient, self).__init__(zk_addrs, znode)
		except:
			log.exception('gds_redis_client_zookeeper_error|zk_addrs=%s,znode=%s', zk_addrs, znode)
			raise GdsClientError('Illegal zookeeper zonfig')

		try:
			redis_config = ET.fromstring(self._config).find('redis')
			host = redis_config.find('ip').text
			port = int(redis_config.find('port').text)
			db = int(redis_config.find('db').text)
		except:
			log.exception('gds_redis_client_config_error|id=%s,config=%s', self._id, self._config)
			raise GdsClientError('Illegal redis config')

		self._redis = redis.StrictRedis(host=host, port=port, db=db)
		try:
			self._redis.get('0')
		except:
			log.exception('gds_redis_client_connect_fail|id=%s,host=%s,port=%d,db=%d', self._id, host, port, db)
			raise GdsClientError('Connect redis failed')

		self._date_offset = 0
		self._seq_offset = 1
		if offset is not None:
			date_str, seq_str = offset.split('.')
			self._seq_offset = int(seq_str)
			self._date_offset = int(date_str)
		else:
			# Fetch latest date and seq when offset is None
			for date_str in self._redis.zrangebyscore(GdsRedisClient.DATE_KEY, self._date_offset, GdsRedisClient.MAX_DATE):
				self._date_offset = int(date_str)

			seq_key = GdsRedisClient.SEQ_KEY_FORMAT % (self._date_offset, )
			seq_max = self._redis.get(seq_key)
			if seq_max is not None:
				self._seq_offset = int(seq_max)

	def consume(self, call_back, row_parser=None):
		"""
		Parameters
		----------
		call_back : function
			Pass offset(int) and gds record item(GdsRecord) to call_back function
		row_parser : function
			Pass table_name(string) and origin_row(dict) to row_parser function,
			return value of row_parser would become row fields in gds record item(GdsRecord).
			If it is None, would use origin_row(dict) as row fields.
		"""
		while True:
			try:
				if self._iterate_all_key(call_back, row_parser) <= 0:
					# sleep 10 millsecond
					time.sleep(0.01)
			except:
				log.exception('gds_redis_client_consume_error|id=%s', self._id)

	def _iterate_all_key(self, call_back, row_parser):
		total_event = 0
		for date_str in self._redis.zrangebyscore(GdsRedisClient.DATE_KEY, self._date_offset, GdsRedisClient.MAX_DATE):
			date = int(date_str)
			if self._date_offset != date:
				self._date_offset = date
				self._seq_offset = 0

			seq_key = GdsRedisClient.SEQ_KEY_FORMAT % (date_str, )
			seq_max = self._redis.get(seq_key)
			if seq_max is None:
				log.error('gds_redis_client_get_last_index_fail|id=%s,seq_key=%s', self._id, seq_key)
				return -1

			seq_max = int(seq_max)
			if seq_max < self._seq_offset:
				log.error('gds_redis_client_unexpected_seq_max|id=%s,seq_max=%d,seq_offset=%d', self._id, seq_max, self._seq_offset)
				continue
			for i in range(self._seq_offset + 1, seq_max):
				if self._seq_offset != i:
					self._seq_offset = i

				k = GdsRedisClient.VAL_KEY_FORMAT % (date_str, i)
				for _ in range(GdsRedisClient.RETRY_TIMES):
					v = self._redis.get(k)
					if v is not None:
						break
					else:
						time.sleep(0.01)
				if v is None:
					log.error('gds_redis_client_value_none|id=%s,key=%s', self._id, k)
					continue

				record = GdsRecord.parse_from(v, row_parser)
				if record is None:
					log.error('gds_redis_client_value_invalid|id=%s,key=%s,value=%s', self._id, k, v)
				total_event += 1

				try:
					call_back('%s.%d' % (date_str, i), record)
				except:
					log.exception('gds_redis_client_consume_error|id=%s', self._id)

		return total_event


class GdsKafkaClient(GdsBaseClient):
	"""
		about offset:
			using OFFSET_BEGIN or OFFSET_END will seek you to location
			if sending unsigned integer n(>=0), will seek you to BEGIN + n
			when you setup a offset, kafka will keep this offset for group

		about kafka offset auto-save:
			while reading you crashed, kafka will now save the last position for you.
			while read finish, and waiting for new msg, kafka will keep this new offset for group.
	"""
	OFFSET_BEGIN = -2
	OFFSET_END = -1
	OFFSET_STORED = -1000

	def __init__(self, zk_addrs, znode, consumer_group, offset=OFFSET_STORED, row_parser=None):
		"""
		Parameters
		----------
		zk_addrs : string
			Zookeeper hosts. Example: "10.232.98.31:2181,10.232.98.32:3181"
		znode : string
			Zookeeper znode. Example: "/gds/test_db"
		consumer_group : string
			Kafka Consumer Group. Example: "test_db_sync"
		offset : int
			Kafka offset
		row_parser : function
			Pass table_name(string) and origin_row(dict) to row_parser function,
			return value of row_parser would become row fields in gds record item(GdsRecord).
			If it is None, would use origin_row(dict) as row fields.
		"""
		try:
			super(GdsKafkaClient, self).__init__(zk_addrs, znode)
		except:
			log.exception('gds_kafka_client_zookeeper_error|zk_addrs=%s,znode=%s', zk_addrs, znode)
			raise

		try:
			kafka_config = ET.fromstring(self._config).find('kafka')
			brokers = kafka_config.find('brokers').text
			topic = kafka_config.find('topic').text
			partition = int(kafka_config.find('partition').text)
		except:
			log.exception('gds_kafka_client_config_error|id=%s,config=%s', self._id, self._config)
			raise

		try:
			# Try to import the high performance kafka consumer client if all dependencies satisfied.
			import confluent_kafka	# pylint: disable=unused-variable
			self._kafka_consumer = RdKafkaConsumer(brokers, topic, partition, consumer_group, offset)
		except:
			self._kafka_consumer = KafkaConsumer(brokers, topic, partition, consumer_group, offset)

		self._row_parser = row_parser

	def commit(self):
		"""
		Use to save the consume offset.
		:return:
		"""
		self._kafka_consumer.commit()

	def _consume(self, call_back, offset, record):
		while True:
			try:
				return call_back(offset, record)
			except:
				# When call_back errors, we would keep retry.
				log.exception('gds_kafka_client_callback_error|id=%s,offset=%d,record=%s', self._id, offset, record)

	def consume(self, call_back, row_parser=None):
		"""
		Parameters
		----------
		call_back : function
			Pass offset(int) and gds record item(GdsRecord) to call_back function
		row_parser : function
			Pass table_name(string) and origin_row(dict) to row_parser function,
			return value of row_parser would become row fields in gds record item(GdsRecord).
			If it is None, would fall back to use `row_parser` passed in constructor.
		"""
		if row_parser is None:
			row_parser = self._row_parser

		for offset, value in self._kafka_consumer.consume():
			record = GdsRecord.parse_from(value, row_parser)
			if record is None:
				log.error('gds_kafka_client_value_invalid|id=%s,offset=%d,value=%s', self._id, offset, value)
			else:
				# call_back(offset, record)
				self._consume(call_back, offset, record)

	def __iter__(self):
		"""
		Noted that `kafka_consumer` save offset after `yield`, so the last item may duplicate if
		you use following code:

		```
		for offset, record in gds_client:
			handle(offset, record)
			if exit_flag:
				break
		```

		To avoid this, we suggest to check the `exit_flag` first before consume the message.

		```
		for offset, record in gds_client:
			if exit_flag:
				break
			handle(offset, record)
		```
		"""
		for offset, value in self._kafka_consumer.consume():
			record = GdsRecord.parse_from(value, self._row_parser)
			if record is None:
				log.error('gds_kafka_client_value_invalid|id=%s,offset=%d,value=%s', self._id, offset, value)
			else:
				yield offset, record
