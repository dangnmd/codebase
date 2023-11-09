from common.service.serviceclient import *


class RewardServiceException(ServiceClientException):
	pass


class RewardServiceBadStatus(ServiceClientBadStatus, RewardServiceException):
	pass


class RewardServiceTimeout(ServiceClientTimeout, RewardServiceBadStatus):
	pass


class RewardServiceClient(ServiceClientClient):
	GENERAL_EXCEPTION_CLS = RewardServiceException
	BAD_STATUS_EXCEPTION_CLS = RewardServiceBadStatus
	TIMEOUT_EXCEPTION_CLS = RewardServiceTimeout
	SERVICE_NAME = "reward_service"

	class Result(object):
		SUCCESS = "success"
		ERROR_PARAMS = "error_params"
		ERROR_HEADER = "error_header"
		ERROR_SERVER = "error_server"
		ERROR_USER_TOKEN = "error_user_token"
		ERROR_SIGNATURE = "error_signature"
		ERROR_CAMPAIGN_CHANGE = "error_campaign_change"
		ERROR_COIN_TRANSACTION_FAILED = "error_coin_transaction_failed"
		ERROR_COIN_TRANSACTION_EXISTS = "error_coin_transaction_exists"

	class Api(object):
		GET_COIN_URL = "/s2s/reward/get_coin"
		GET_INFO_URL = "/s2s/reward/get_info"
		VALIDATE_URL = "/s2s/reward/validate"
		EARN_COIN_URL = "/s2s/reward/earn_coin"
		REFUND_COIN_URL = "/s2s/reward/refund"
		CANCEL_ORDER_URL = "/s2s/reward/cancel_order"
		GET_ORDER_TRANSACTIONS_URL = "/s2s/reward/get_order_transactions"
		GET_PAYABLE_COIN_URL = "/s2s/reward/get_payable_coin"
		USE_COIN = '/s2s/reward/use_coin'
		GET_PRODUCTS_URL = '/s2s/reward/get_products'
		GET_USER_AVAILABLE_COIN = '/s2s/reward/get_user_available_coin'
		GET_REFERRAL_CAMPAIGN_INFO = '/s2s/reward/get_referral_info'
		NEW_USER = '/s2s/reward/new_user'
		VALIDATE_GIFT_PRODUCT = '/s2s/reward/validate_gift_product'
		APPLY_GIFT_PRODUCT = '/s2s/reward/apply_gift_product'
		GET_ORDER_GIFT_PRODUCT_IDS = '/s2s/reward/get_order_gift_product_ids'
		CANCEL_GIFT_PRODUCT = '/s2s/reward/cancel_gift_product'
		GET_TOTAL_REFERRAL = '/s2s/reward/total_referral'
		GET_GIFT_BY_PRODUCT = '/s2s/reward/get_gift_by_product'
		ADMIN_GET_ORDER_TRANSACTIONS_URL = "/s2s/admin/get_order_transactions"

	def get_coin(self, param):
		return self.request(self.Api.GET_COIN_URL, param)

	def get_info(self, param):
		return self.request(self.Api.GET_INFO_URL, param)

	def validate(self, param):
		return self.request(self.Api.VALIDATE_URL, param)

	def earn_coin(self, param):
		return self.request(self.Api.EARN_COIN_URL, param)
	
	def refund_coin(self, param):
		return self.request(self.Api.REFUND_COIN_URL, param)

	def cancel_order(self, param):
		return self.request(self.Api.CANCEL_ORDER_URL, param)

	def get_order_transactions(self, param):
		return self.request(self.Api.GET_ORDER_TRANSACTIONS_URL, param)

	def get_payable_coin(self, param):
		return self.request(self.Api.GET_PAYABLE_COIN_URL, param)

	def use_coin(self, param):
		return self.request(self.Api.USE_COIN, param)

	def get_products(self, param):
		return self.request(self.Api.GET_PRODUCTS_URL, param)

	def get_user_available_coin(self, param):
		return self.request(self.Api.GET_USER_AVAILABLE_COIN, param)

	def get_referral_campaign_info(self, param):
		return self.request(self.Api.GET_REFERRAL_CAMPAIGN_INFO, param, method="GET")

	def new_user(self, param):
		return self.request(self.Api.NEW_USER, param)

	def validate_gift_product(self, param):
		return self.request(self.Api.VALIDATE_GIFT_PRODUCT, param)

	def apply_gift_product(self, param):
		return self.request(self.Api.APPLY_GIFT_PRODUCT, param)

	def get_order_gift_product_ids(self, param):
		return self.request(self.Api.GET_ORDER_GIFT_PRODUCT_IDS, param)

	def cancel_gift_product(self, param):
		return self.request(self.Api.CANCEL_GIFT_PRODUCT, param)

	def get_total_referral(self, param):
		return self.request(self.Api.GET_TOTAL_REFERRAL, param)

	def get_gift_by_product(self, param):
		return self.request(self.Api.GET_GIFT_BY_PRODUCT, param)

	def get_order_transactions_admin(self, param):
		return self.request(self.Api.ADMIN_GET_ORDER_TRANSACTIONS_URL, param)
