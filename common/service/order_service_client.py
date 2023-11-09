from common.service.serviceclient import *


class OrderServiceException(ServiceClientException):
	pass


class OrderServiceBadStatus(ServiceClientBadStatus, OrderServiceException):
	pass


class OrderServiceTimeout(ServiceClientTimeout, OrderServiceBadStatus):
	pass


class OrderServiceClient(ServiceClientClient):
	GENERAL_EXCEPTION_CLS = OrderServiceException
	BAD_STATUS_EXCEPTION_CLS = OrderServiceBadStatus
	TIMEOUT_EXCEPTION_CLS = OrderServiceTimeout
	SERVICE_NAME = "order_service"

	class Result(object):
		SUCCESS = "success"
		ERROR_PARAMS = "error_params"
		ERROR_HEADER = "error_header"
		ERROR_SERVER = "error_server"
		ERROR_USER_TOKEN = "error_user_token"
		ERROR_SIGNATURE = "error_signature"
		ERROR_CAN_NOT_CREATE = "error_can_not_create"
		ERROR_CAN_NOT_UPDATE = "error_can_not_update"
		ERROR_CAN_NOT_DELETE = "error_can_not_delete"

	class Api(object):
		ORDER_SUBMIT = "/s2s/order/submit"
		ORDER_UPDATE_BASIC_INFO = "/s2s/order/update_basic_info"
		ORDER_GET_INFOS_BY_CODES = "/s2s/order/get_infos_by_codes"
		ORDER_GET_ORDER_IDS_BY_UID = "/s2s/order/get_order_ids_by_uid"
		ORDER_GET_ORDER_REPAY = "/s2s/order/repay"
		ORDER_GET_ORDER_UPDATE_STATUS = "/s2s/order/update_status"
		ORDER_UPDATE_PAYMENT_STATUS = "/s2s/order/update_payment_status"
		ORDER_PAYMENT_CANCEL = "/s2s/order/payment_cancel"

	def submit(self, params, disable_retry=True):
		return self.request(self.Api.ORDER_SUBMIT, params, disable_retry=disable_retry)

	def update_basic_info(self, params, disable_retry=True):
		return self.request(self.Api.ORDER_UPDATE_BASIC_INFO, params, disable_retry=disable_retry)

	def get_infos_by_codes(self, params):
		return self.request(self.Api.ORDER_GET_INFOS_BY_CODES, params)

	def get_order_ids_by_uid(self, params):
		return self.request(self.Api.ORDER_GET_ORDER_IDS_BY_UID, params)

	def repay(self, params):
		return self.request(self.Api.ORDER_GET_ORDER_REPAY, params)

	def update_status(self, params):
		return self.request(self.Api.ORDER_GET_ORDER_UPDATE_STATUS, params)

	def update_payment_status(self, params, disable_retry=True):
		return self.request(self.Api.ORDER_UPDATE_PAYMENT_STATUS, params, disable_retry=disable_retry)

	def payment_cancel(self, params, disable_retry=True):
		return self.request(self.Api.ORDER_PAYMENT_CANCEL, params, disable_retry=disable_retry)
