# pylint: disable=too-many-arguments
import pymssql
from .logger import log

def _wrap_execute(error):
	def __wrap_execute(func):
		def _func(self, sql, *args):
			# pylint: disable=protected-access
			if self._connection is None:
				if not self._connect():
					log.error('mssql_execute_fail|sql=%s,params=%s,exception=connect_fail', sql, repr(args))
					return error
			try:
				return func(self, sql, *args)
			except pymssql.OperationalError as ex:
				self._close()
				if ex[0] == self.ERROR_READ_DATA or ex[0] == self.ERROR_WRITE_DATA:
					log.warn('mssql_execute_error_connection|retry=true')
					try:
						if not self._connect():
							log.error('mssql_execute_fail|sql=%s,params=%s,exception=connect_fail', sql, repr(args))
							return error
						return func(self, sql, *args)
					except:
						self._close()
						log.exception('mssql_execute_fail|sql=%s,params=%s', sql, repr(args))
						return error
				else:
					log.exception('mssql_execute_fail|sql=%s,params=%s', sql, repr(args))
					return error
			except:
				self._close()
				log.exception('mssql_execute_fail|sql=%s,params=%s', sql, repr(args))
				return error
		return _func
	return __wrap_execute

class MssqlClient:

	DEFAULT_TIMEOUT = 2
	ERROR_READ_DATA = 20004
	ERROR_WRITE_DATA = 20006

	def __init__(self, host, port, user, password, db, charset='utf8', result_as_dict=False, timeout=DEFAULT_TIMEOUT):
		self._host = host
		self._port = port
		self._user = user
		self._password = password
		self._db = db
		self._charset = charset
		self._timeout = timeout
		self._result_as_dict = result_as_dict
		self._connection = None
		self._affected_rows = 0
		self._last_insert_id = 0

	@property
	def affected_rows(self):
		return self._affected_rows

	@property
	def last_insert_id(self):
		return self._last_insert_id

	@_wrap_execute(error=None)
	def query(self, sql, *args):
		cursor = self._connection.cursor(as_dict=self._result_as_dict)
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
		log.info('mssyql_try_connect|host=%s,port=%d,user=%s,db=%s', self._host, self._port, self._user, self._db)
		try:
			if self._connection is not None:
				self._connection.close()
			self._connection = pymssql.connect(
				server=self._host,
				port=self._port,
				user=self._user,
				password=self._password,
				database=self._db,
				charset=self._charset,
				timeout=self._timeout
			)
			self._connection.autocommit(True)
			log.info('mssql_connect_success|host=%s,port=%d,db=%s', self._host, self._port, self._db)
			return True
		except Exception as ex:
			log.exception('mssql_connect_fail|host=%s,port=%d,db=%s,exception=%s', self._host, self._port, self._db, ex)
			self._connection = None
			self._affected_rows = 0
			return False
