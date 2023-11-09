from common.service.serviceclient import *


class NotifyServiceException(ServiceClientException):
	pass


class NotifyServiceBadStatus(ServiceClientBadStatus, NotifyServiceException):
	pass


class NotifyServiceTimeout(ServiceClientTimeout, NotifyServiceBadStatus):
	pass


class NotifyServiceClient(ServiceClientClient):
	GENERAL_EXCEPTION_CLS = NotifyServiceException
	BAD_STATUS_EXCEPTION_CLS = NotifyServiceBadStatus
	TIMEOUT_EXCEPTION_CLS = NotifyServiceTimeout
	SERVICE_NAME = "notify_service"

	class Result(object):
		SUCCESS = "success"
		ERROR_PARAMS = "error_params"
		ERROR_HEADER = "error_header"
		ERROR_SERVER = "error_server"
		ERROR_USER_TOKEN = "error_user_token"
		ERROR_SIGNATURE = "error_signature"

	class Api(object):
		SEND_EMAIL = "/s2s/email/send"
		SEND_SMS = "/s2s/sms/send"
		SEND_TO_USERS = "/s2s/notify/send_to_users"

	def send_email(self, param):
		return self.request(self.Api.SEND_EMAIL, param)

	def send_sms(self, param):
		return self.request(self.Api.SEND_SMS, param)

	def notify_send_to_users(self, param):
		return self.request(self.Api.SEND_TO_USERS, param)
