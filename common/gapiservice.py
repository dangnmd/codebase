import struct
import time
from .logger import log
from . import gtcpclient
from . import jsonutils
from . import crypt

class ApiServiceError(Exception):
	def __init__(self, error):
		super(ApiServiceError, self).__init__(error)
		self.error = error
	def __str__(self):
		return self.error

class GApiServiceClient(object):

	def __init__(self, address, port, app_id, app_key=None, timeout=10):
		self._client = gtcpclient.GTcpClient(address, port, timeout)
		self._app_id = app_id
		self._app_id_bytes = struct.pack('<I', app_id)
		self._app_key = app_key
		self._id = 0

	def request(self, api, params):
		now = int(time.time())
		self._id = (self._id + 1) % 0xffffffff
		request_id = str(self._id)
		request = {'id': request_id, 'time': now, 'api': api, 'params': params}
		request_body = jsonutils.to_json(request)
		if isinstance(request_body, str):
			request_body = request_body.encode('utf-8')
		if self._app_key:
			request_body = crypt.garena_aes_encrypt(request_body, self._app_key)
		request_bytes = self._app_id_bytes + request_body
		reply_bytes = self._client.request(request_bytes)
		reply_body = ''
		try:
			if reply_bytes is None:
				raise Exception('no_reply')
			if not reply_bytes.startswith(self._app_id_bytes):
				raise Exception('reply_header_error')
			reply_body = reply_bytes[len(self._app_id_bytes):]
			if self._app_key:
				reply_body = crypt.garena_aes_decrypt(reply_body, self._app_key)
			if reply_body is None:
				reply_body = reply_bytes.encode('hex')
				raise Exception('reply_decrypt_error')
			reply_data = jsonutils.from_json(reply_body)
			if reply_data['id'] != request_id:
				raise Exception('reply_header_error')
			error_code = reply_data.get('error', None)
			result = reply_data.get('result', None)
			log.data('api_request|id=%d,api=%s,params=%s,error=%s', self._id, api, jsonutils.to_json(params), error_code)
			return error_code, result
		except Exception as ex:
			self._client.close()
			log.error('api_request_fail|id=%d,api=%s,params=%s,reply=%s,error=%s', self._id, api, jsonutils.to_json(params), reply_body, ex)
			return 'error_unknown', None

	#this function will raise ApiServiceError if request failed
	def request_ex(self, api, params):
		error_code, result = self.request(api, params)
		if error_code:
			raise ApiServiceError(error_code)
		return result
