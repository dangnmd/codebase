from common.service.serviceclient import *


class PromotionServiceException(ServiceClientException):
	pass


class PromotionServiceBadStatus(ServiceClientBadStatus, PromotionServiceException):
	pass


class PromotionServiceTimeout(ServiceClientTimeout, PromotionServiceBadStatus):
	pass


class PromotionServiceClient(ServiceClientClient):
	GENERAL_EXCEPTION_CLS = PromotionServiceException
	BAD_STATUS_EXCEPTION_CLS = PromotionServiceBadStatus
	TIMEOUT_EXCEPTION_CLS = PromotionServiceTimeout
	SERVICE_NAME = "promotion_service"

	class Result(object):
		SUCCESS = "success"
		ERROR_PARAMS = "error_params"
		ERROR_HEADER = "error_header"
		ERROR_SERVER = "error_server"
		ERROR_FORBIDDEN = "error_forbidden"
		ERROR_DATA_NOT_EXISTS = "error_data_not_exists"
		ERROR_UPDATE_FAILED = "error_update_failed"
		ERROR_DEFINED_MESSAGE = "error_defined_message"
		ERROR_INVALID_DATA = "error_invalid_data"
		ERROR_RELATIONSHIP_DATA = "error_relationship_data"
		ERROR_APPLIED_PROMOTION = "error_applied_promotion"
		ERROR_INVALID_PROMOTION = "error_invalid_promotion"
		ERROR_CHANGED_PROMOTION = "error_promotion_changed"

	class Api(object):
		GET_BY_PRODUCTS_URL = "/s2s/promotion/get_by_products"
		GET_BY_CART_PRODUCTS_URL = "/s2s/promotion/get_by_cart_products"
		VALIDATE_URL = "/s2s/promotion/validate"
		APPLY_URL = "/s2s/promotion/apply"
		CANCEL_URL = "/s2s/promotion/cancel"
		GET_AVAILABLE_CODES_URL = "/s2s/promotion/get_available_codes"
		GET_ORDER_PROMOTIONS_URL = "/s2s/promotion/get_order_promotions"
		GET_FLASH_SALE_PRODUCTS_URL = "/s2s/promotion/get_flash_sale_products"
		GET_FLASH_SALE_INFOS_URL = "/s2s/promotion/get_flash_sale_infos"
		GET_USER_AVAILABLE_CODES_URL = "/s2s/promotion/get_user_available_codes"
		GET_PUBLIC_VOUCHERS_URL = "/s2s/promotion/get_public_vouchers"

	def get_by_products(self, param):
		return self.request(self.Api.GET_BY_PRODUCTS_URL, param)

	def get_by_cart_products(self, param):
		return self.request(self.Api.GET_BY_CART_PRODUCTS_URL, param)

	def validate(self, param):
		return self.request(self.Api.VALIDATE_URL, param)

	def apply(self, param):
		return self.request(self.Api.APPLY_URL, param)

	def cancel(self, param):
		return self.request(self.Api.CANCEL_URL, param)

	def get_available_codes(self, param):
		return self.request(self.Api.GET_AVAILABLE_CODES_URL, param)

	def get_order_promotions(self, param):
		return self.request(self.Api.GET_ORDER_PROMOTIONS_URL, param)

	def get_flash_sale_products(self, param):
		return self.request(self.Api.GET_FLASH_SALE_PRODUCTS_URL, param)

	def get_flash_sale_infos(self, param):
		return self.request(self.Api.GET_FLASH_SALE_INFOS_URL, param)

	def get_user_available_codes(self, param):
		return self.request(self.Api.GET_USER_AVAILABLE_CODES_URL, param)

	def get_public_vouchers(self, param):
		return self.request(self.Api.GET_PUBLIC_VOUCHERS_URL, param)
