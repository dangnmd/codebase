# pylint: disable=too-many-arguments
import MySQLdb
import MySQLdb.cursors
from .logger import log
from _mysql_exceptions import OperationalError

def _wrap_execute(error):
	def __wrap_execute(func):
		def _func(self, sql, *args):
			# pylint: disable=protected-access
			if self._connection is None:
				if not self._connect():
					log.error('mysql_execute_fail|sql=%s,params=%s,exception=connect_fail', sql, repr(args))
					return error
			try:
				return func(self, sql, *args)
			except OperationalError as ex:
				self._close()
				if ex[0] == self.ERROR_LOST_CONNECTION:
					log.warn('mysql_execute_lost_connection|retry=true')
					try:
						if not self._connect():
							log.error('mysql_execute_fail|sql=%s,params=%s,exception=connect_fail', sql, repr(args))
							return error
						return func(self, sql, *args)
					except:
						self._close()
						log.exception('mysql_execute_fail|sql=%s,params=%s', sql, repr(args))
						return error
				else:
					log.exception('mysql_execute_fail|sql=%s,params=%s', sql, repr(args))
					return error
			except:
				self._close()
				log.exception('mysql_execute_fail|sql=%s,params=%s', sql, repr(args))
				return error
		return _func
	return __wrap_execute

class MysqlClient:

	DEFAULT_TIMEOUT = 2
	ERROR_LOST_CONNECTION = 2006
	RESULT_TYPE_TUPLE = MySQLdb.cursors.Cursor
	RESULT_TYPE_DICT = MySQLdb.cursors.DictCursor

	def __init__(self, host, port, user, password, db, charset='utf8', result=RESULT_TYPE_TUPLE, timeout=DEFAULT_TIMEOUT, use_unicode=True):
		self._host = host
		self._port = port
		self._user = user
		self._password = password
		self._db = db
		self._charset = charset
		self._timeout = timeout
		self._cursor = result
		self._connection = None
		self._affected_rows = 0
		self._last_insert_id = 0
		self._use_unicode = use_unicode

	@property
	def affected_rows(self):
		return self._affected_rows

	@property
	def last_insert_id(self):
		return self._last_insert_id

	@staticmethod
	def escape_string(s):
		return MySQLdb.escape_string(s)

	@_wrap_execute(error=None)
	def query(self, sql, *args):
		cursor = self._connection.cursor(cursorclass=self._cursor)
		cursor.execute(sql, args)
		data = cursor.fetchall()
		self._affected_rows = cursor.rowcount
		cursor.close()
		return data

	@_wrap_execute(error=False)
	def execute(self, sql, *args):
		cursor = self._connection.cursor()
		cursor.execute(sql, args)
		self._affected_rows = cursor.rowcount
		self._last_insert_id = cursor.lastrowid
		cursor.close()
		return True

	@_wrap_execute(error=False)
	def execute_many(self, sql, args):
		cursor = self._connection.cursor()
		cursor.executemany(sql, args)
		self._affected_rows = cursor.rowcount
		cursor.close()
		return True

	def _close(self):
		if self._connection is not None:
			self._connection.close()
			self._connection = None
			self._affected_rows = 0

	def _connect(self):
		log.info('msyql_try_connect|host=%s,port=%d,user=%s,db=%s', self._host, self._port, self._user, self._db)
		try:
			if self._connection is not None:
				self._connection.close()
			self._connection = MySQLdb.connect(
				host=self._host,
				port=self._port,
				user=self._user,
				passwd=self._password,
				db=self._db,
				charset=self._charset,
				connect_timeout=self._timeout,
				use_unicode=self._use_unicode
			)
			self._connection.autocommit(True)
			log.info('mysql_connect_success|host=%s,port=%d,db=%s', self._host, self._port, self._db)
			return True
		except Exception as ex:
			log.exception('mysql_connect_fail|host=%s,port=%d,db=%s,exception=%s', self._host, self._port, self._db, ex)
			self._connection = None
			self._affected_rows = 0
			return False
