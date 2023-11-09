# pylint: disable=too-many-arguments
from . import gtcpclient
from .pbdata import pns_pb2
from .logger import log
from .pbutils import pb_to_str

class PushNotificationService(object):

	CLIENT_TYPE_IOS = pns_pb2.TYPE_IOS
	CLIENT_TYPE_ANDROID = pns_pb2.TYPE_ANDROID

	SERVICE_TYPE_APNS = pns_pb2.SERVICE_APNS
	SERVICE_TYPE_GPNS = pns_pb2.SERVICE_GPNS
	SERVICE_TYPE_GCMS = pns_pb2.SERVICE_GCMS

	PRIORITY_LEVEL_HIGH = pns_pb2.PRIORITY_HIGH
	PRIORITY_LEVEL_NORMAL = pns_pb2.PRIORITY_NORMAL

	TIMEOUT = 10

	def __init__(self, ip, port, app_id):
		self._client = gtcpclient.GTcpClient(ip, port, self.TIMEOUT)
		self._app_id = app_id

	def push_notification(self, client_type, token, message,
		data=None, badge=None, sound=None, expire_time=None, service_type=None, priority=None):
		request = pns_pb2.Notification()
		request.app_id = self._app_id
		request.client_type = client_type
		request.device_token = token
		request.message = message
		if data is not None:
			request.data = data
		if badge is not None:
			request.badge = badge
		if sound is not None:
			request.sound = sound
		if expire_time is not None:
			request.expire_time = expire_time
		if service_type is not None:
			request.service_type = service_type
		if priority is not None:
			request.priority = priority
		reply = self._request(pns_pb2.CMD_PUSH_NOTIFICATION, request, pns_pb2.PNSResponse)
		if reply is None:
			log.error('pns_push_fail|client_type=%d,token=%s,message=%s,error=request_error', client_type, token.encode('hex'), message)
			return False
		if reply.error_code != pns_pb2.PNSResponse.PNS_SUCCESS:
			log.error('pns_push_fail|client_type=%d,token=%s,message=%s,error=%d', client_type, token.encode('hex'), message, reply.error_code)
			return False
		log.data('pns_push_notification|client_type=%d,token=%s,message=%s,data=%s', client_type, token.encode('hex'), message, data)
		return True

	def get_invalid_tokens(self, client_type, service_type=None):
		request = pns_pb2.InvalidTokenQuery()
		request.app_id = self._app_id
		request.client_type = client_type
		if service_type is not None:
			request.service_type = service_type
		reply = self._request(pns_pb2.CMD_QUERY_INVALID_TOKENS, request, pns_pb2.InvalidTokens)
		if reply is None:
			return None
		return [token.device_token for token in reply.tokens]

	def update_app(self):
		"""Reload pem file and GCM key

		This method should be called when the pem file or GCM key is changed. PNS Sever will reload pem file/GCM key and reconnect to the push services.
		"""
		request = pns_pb2.AppUpdateRequest()
		request.app_id = self._app_id
		reply = self._request(pns_pb2.CMD_APP_UPDATE, request, pns_pb2.PNSResponse)
		if reply is None:
			log.error('update_app_request_fail|app_id=%s', self._app_id)
			return False
		if reply.error_code != pns_pb2.PNSResponse.PNS_SUCCESS:
			log.error('update_app_fail|app_id=%s', self._app_id)
			return False
		return True

	def _request(self, cmd, request, reply_type):
		try:
			cmd_data = chr(cmd)
			request_data = cmd_data + request.SerializePartialToString()
			reply = self._client.request(request_data)
			if not reply:
				self._client.close()
				raise Exception('reply_error')
			if reply[0] != cmd_data:
				self._client.close()
				raise Exception('reply_cmd_error')
			if reply_type is None:
				return reply[1:]
			else:
				return reply_type.FromString(reply[1:])
		except Exception as ex:
			log.exception('pns_request_fail|cmd=%d,request=%s,exception=%s', cmd, pb_to_str(request), ex)
			return None
