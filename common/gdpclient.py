import queue
from .logger import log
from .gtcpclient import GTcpClient
from google.protobuf import message
from .pbdata import GdpProtocol_pb2

def pb_to_short_str(pb):
	return str(pb).replace('\n', ', ')

class GDPClient:

	DEFAULT_TIMEOUT = 5
	MAX_REQUEST_PACKET_SIZE = 256 * 1024
	MAX_REPLY_PACKET_SIZE = 1024 * 1024

	def __init__(self, client_id, ip, port, timeout=DEFAULT_TIMEOUT):
		self._client_id = client_id
		self._client = GTcpClient(ip, port, timeout)
		self._request_id = 0

	def query(self, request):
		if not request.HasField('id'):
			request.id = self._get_request_id()
		request_data = request.SerializeToString()
		if len(request_data) > self.MAX_REQUEST_PACKET_SIZE:
			log.error('gdp_query_fail|error=request_size_overflow,client=%s,request=%s', self._client_id, pb_to_short_str(request))
			return None
		reply_data = self._client.request(request_data)
		if reply_data is None:
			log.error('gdp_query_fail|error=request_fail,client=%s,request=%s', self._client_id, pb_to_short_str(request))
			return None
		if len(reply_data) > self.MAX_REPLY_PACKET_SIZE:
			log.error('gdp_query_fail|error=reply_size_overflow,client=%s,request=%s', self._client_id, pb_to_short_str(request))
			return None
		try:
			reply = GdpProtocol_pb2.Reply.FromString(reply_data)
		except Exception as ex:
			log.exception('gdp_query_fail|error=parse_reply_fail,client=%s,request=%s,reply=%s,ex=%s',
				self._client_id, pb_to_short_str(request), reply_data.encode('hex'), ex)
			self._client.close()
			return None
		if not reply.IsInitialized():
			log.error('gdp_query_fail|error=reply_data_error,client=%s,request=%s,reply=%s',
				self._client_id, pb_to_short_str(request), reply_data.encode('hex'))
			self._client.close()
			return None
		if request.id != reply.id:
			log.error('gdp_query_fail|error=reply_id_mismatch,client=%s,request=%s,reply=%s',
				self._client_id, pb_to_short_str(request), pb_to_short_str(reply))
			self._client.close()
			return None
		if len(request.queries) != len(reply.results):
			log.error('gdp_query_fail|error=reply_results_mismatch,client=%s,request=%s,reply=%s',
				self._client_id, request, pb_to_short_str(reply))
			self._client.close()
			return None
		return reply

	def _get_request_id(self):
		self._request_id = (self._request_id + 1) % 0xffffffff
		return self._request_id

class GDPClientManager:

	def __init__(self, config):
		self._clients = {}
		self._default_client_id = None
		first = True
		for client_id in config:
			client_config = config[client_id]
			if 'count' in client_config:
				count = client_config['count']
			else:
				count = 1
			if 'timeout' in client_config:
				timeout = client_config['timeout']
			else:
				timeout = GDPClient.DEFAULT_TIMEOUT
			client_queue = queue.Queue()
			for i in range(count):
				client_queue.put(GDPClient(client_id + '.' + str(i), client_config['ip'], client_config['port'], timeout))
			self._clients[client_id] = client_queue
			if first or ('default' in client_config and client_config['default']):
				first = False
				self._default_client_id = client_id

	def query(self, request, client_id=None):
		if client_id is None:
			client_id = self._default_client_id
		if client_id not in self._clients:
			log.error('gdp_query_unknow_client|client=%s,request=%s', client_id, pb_to_short_str(request))
			return None
		client_queue = self._clients[client_id]
		client = client_queue.get()
		reply = client.query(request)
		client_queue.put(client)
		return reply

gdp_client_manager = None

def init_gdp_client_manager(config):
	global gdp_client_manager	# pylint: disable=global-statement
	gdp_client_manager = GDPClientManager(config)

def gdp_query(request, client_id=None):
	global gdp_client_manager	# pylint: disable=global-statement
	if gdp_client_manager is None:
		log.error('gdp_query_not_init|client=%s,request=%s', client_id, request)
		return None
	return gdp_client_manager.query(request, client_id)

class GdpQuery:

	NO_RESULT = 0
	OPTIONAL_RESULT = 1
	SINGLE_RESULT = 2
	MULTI_RESULT = 3

	STATUS_SUCCESS = GdpProtocol_pb2.Result.STATUS_SUCCESS
	STATUS_ERROR = GdpProtocol_pb2.Result.STATUS_ERROR
	STATUS_ERROR_SERVER = GdpProtocol_pb2.Result.STATUS_ERROR_SERVER
	STATUS_ERROR_AUTH = GdpProtocol_pb2.Result.STATUS_ERROR_AUTH
	STATUS_ERROR_PARAM = GdpProtocol_pb2.Result.STATUS_ERROR_PARAM
	STATUS_ERROR_CONFIG = GdpProtocol_pb2.Result.STATUS_ERROR_CONFIG
	STATUS_ERROR_STORAGE = GdpProtocol_pb2.Result.STATUS_ERROR_STORAGE
	STATUS_ERROR_DATA = GdpProtocol_pb2.Result.STATUS_ERROR_DATA
	STATUS_ERROR_NO_DATA = GdpProtocol_pb2.Result.STATUS_ERROR_NO_DATA
	STATUS_ERROR_EXIST = GdpProtocol_pb2.Result.STATUS_ERROR_EXIST
	STATUS_ERROR_NOT_EXIST = GdpProtocol_pb2.Result.STATUS_ERROR_NOT_EXIST

	TABLE_STATUS_TO_STRING = dict((v, k) for k, v in list(vars(GdpProtocol_pb2.Result).items()) if k.startswith('STATUS_'))

	PARAMS_TYPE = None
	RESULT_COUNT = NO_RESULT

	def __init__(self, *params, **kwparams):
		self.add_params(*params, **kwparams)
		self.option = 0
		self.success = False
		self.status = self.STATUS_ERROR
		self.result = None

	def __str__(self):
		if isinstance(self.PARAMS_TYPE, (tuple, list)):
			params = []
			for param in self.params:
				if isinstance(param, str):
					params.append(param.encode('utf-8'))
				else:
					params.append(str(param))
			params_str = ','.join(params)
		elif isinstance(self.params, message.Message):
			params_str = pb_to_short_str(self.params)
		else:
			params_str = str(self.params)
		return '%s(%s)' % (self.QUERY_NAME, params_str)

	def __repr__(self):
		return self.__str__()

	def add_params(self, *params, **kwparams):
		if self.PARAMS_TYPE is None:
			if params:
				raise Exception('params_error')
			self.params = None
		elif isinstance(self.PARAMS_TYPE, (tuple, list)):
			if params:
				self.params = params
			else:
				self.params = []
		else:
			if not params:
				if issubclass(self.PARAMS_TYPE, message.Message):
					self.params = self.PARAMS_TYPE(**kwparams)
				else:
					self.params = None
			elif len(params) == 1 and self._is_match_type(params[0], self.PARAMS_TYPE):
				self.params = params[0]
			else:
				raise Exception('params_error')

	def set_query_from_db(self, enable):
		if enable:
			self.option |= GdpProtocol_pb2.Query.OPTION_QUERY_FROM_DB
		else:
			self.option &= ~GdpProtocol_pb2.Query.OPTION_QUERY_FROM_DB

	def set_query_from_master(self, enable):
		if enable:
			self.option |= GdpProtocol_pb2.Query.OPTION_QUERY_FROM_MASTER
		else:
			self.option &= ~GdpProtocol_pb2.Query.OPTION_QUERY_FROM_MASTER

	def run(self, client_id=None):
		self.success = False
		self.status = self.STATUS_ERROR
		request = GdpProtocol_pb2.Request()
		query = request.queries.add()
		if not self.set_query(query):
			self.status = self.STATUS_ERROR_PARAM
			log.error('gdp_query_params_error|query=%s', pb_to_short_str(query))
			return False
		reply = gdp_query(request, client_id)
		if reply is None:
			self.status = self.STATUS_ERROR_SERVER
			log.error('gdp_query_fail|query=%s', pb_to_short_str(query))
			return False
		if not self.set_result(reply.results[0]):
			log.error('gdp_query_set_result_fail|query=%s,result=%s', pb_to_short_str(query), pb_to_short_str(reply.results[0]))
			return False
		return True

	def set_query(self, query):
		query.name = self.QUERY_NAME
		query.option = self.option
		if self.PARAMS_TYPE is None:
			if self.params is not None:
				if not isinstance(self.params, (tuple, list)) or self.params:
					return False
		elif isinstance(self.PARAMS_TYPE, (tuple, list)):
			if len(self.PARAMS_TYPE) != len(self.params):
				return False
			for i in range(len(self.PARAMS_TYPE)):
				if not self._append_query_param(query, self.params[i], self.PARAMS_TYPE[i]):	# pylint: disable=unsubscriptable-object
					return False
		elif not self._append_query_param(query, self.params, self.PARAMS_TYPE):
			return False
		return True

	def set_result(self, result):
		self.status = result.status
		if self.status != self.STATUS_SUCCESS:
			return False
		count = len(result.data)
		if self.RESULT_COUNT == self.NO_RESULT:
			if count != 0:
				self.status = self.STATUS_ERROR_DATA
				return False
		elif self.RESULT_COUNT == self.OPTIONAL_RESULT:
			if count > 1:
				self.status = self.STATUS_ERROR_DATA
				return False
			if count == 1:
				try:
					self.result = self.RESULT_TYPE.FromString(result.data[0])
				except:
					self.status = self.STATUS_ERROR_DATA
					return False
		elif self.RESULT_COUNT == self.SINGLE_RESULT:
			if count != 1:
				if count == 0:
					self.status = self.STATUS_ERROR_NO_DATA
				else:
					self.status = self.STATUS_ERROR_DATA
				return False
			try:
				self.result = self.RESULT_TYPE.FromString(result.data[0])
			except:
				self.status = self.STATUS_ERROR_DATA
				return False
		elif self.RESULT_COUNT == self.MULTI_RESULT:
			self.result = []
			try:
				for data in result.data:
					self.result.append(self.RESULT_TYPE.FromString(data))
			except:
				self.status = self.STATUS_ERROR_DATA
				return False
		else:
			return False
		self.success = True
		return True

	def get_status_str(self):
		if self.status in self.TABLE_STATUS_TO_STRING:
			return self.TABLE_STATUS_TO_STRING[self.status]
		return 'STATUS_UNKNOW'

	def _is_match_type(self, obj, expect_type):
		if isinstance(obj, expect_type):
			return True
		elif expect_type is str:
			return isinstance(obj, str)
		elif expect_type is str:
			return isinstance(obj, str)
		elif expect_type is int:
			return isinstance(obj, int) and -0x80000000 <= obj <= 0xffffffff
		elif expect_type is int:
			return isinstance(obj, int)
		elif expect_type is float:
			return isinstance(obj, [int, int])
		return False

	def _append_query_param(self, query, param, param_type):
		if not self._is_match_type(param, param_type):
			return False
		if isinstance(param, message.Message):
			query.params.append(param.SerializeToString())
			return True
		if isinstance(param, str):
			query.params.append(param.encode('utf-8'))
			return True
		query.params.append(str(param))
		return True

class GdpBatchQuery:

	MAX_QUERY_COUNT_PER_REQUEST = 50

	def __init__(self, *queries):
		self.queries = []
		self.add(*queries)
		self.all_success = False

	def __iter__(self):
		return self.queries.__iter__()

	def add(self, *queries):
		for query in queries:
			if isinstance(query, (tuple, list)):
				for query_item in query:
					if isinstance(query_item, GdpQuery):
						self.queries.append(query_item)
					else:
						raise Exception('invalid_query')
			elif isinstance(query, GdpQuery):
				self.queries.append(query)
			else:
				raise Exception('invalid_query')

	def clear(self):
		self.queries = []
		self.all_success = False

	def is_empty(self):
		return not self.queries

	def run(self, client_id=None):
		queries_count = len(self.queries)
		end_index = queries_count - 1
		real_queries = []
		request = GdpProtocol_pb2.Request()
		query_round = 0
		for i in range(queries_count):
			query = self.queries[i]
			query.success = False
			query.status = GdpQuery.STATUS_ERROR
			query_pb = GdpProtocol_pb2.Query()
			if query.set_query(query_pb):
				request.queries.extend([query_pb])
				real_queries.append(query)
			else:
				log.error('gdp_batch_query_params_error|index=%d,query=%s', i, query)
				query.status = GdpQuery.STATUS_ERROR_PARAM
			if (i >= end_index and request.queries) or len(request.queries) >= self.MAX_QUERY_COUNT_PER_REQUEST:
				reply = gdp_query(request, client_id)
				if reply is None:
					for query in real_queries:
						query.status = GdpQuery.STATUS_ERROR_SERVER
					log.error('gdp_batch_query_fail|round=%d,queries=%d', query_round, len(real_queries))
				elif len(real_queries) != len(reply.results):
					log.error('gdp_batch_query_result_mismatch|round=%d,queries=%d,results=%d', query_round, len(real_queries), len(reply.results))
				else:
					for j in range(len(real_queries)):
						if not real_queries[j].set_result(reply.results[j]):
							log.error('gdp_batch_query_set_result_fail|index=%d,query=%s,result=%s', i, real_queries[j], pb_to_short_str(reply.results[j]))
				real_queries = []
				request.Clear()
				query_round += 1

		self.all_success = True
		for i in range(queries_count):
			query = self.queries[i]
			if not query.success:
				log.error('gdp_batch_query_error|index=%d,query=%s', i, query)
				self.all_success = False
		return self.all_success
