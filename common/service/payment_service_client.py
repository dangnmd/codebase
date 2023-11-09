from common.service.serviceclient import *


class PaymentServiceException(ServiceClientException):
    pass


class PaymentServiceBadStatus(ServiceClientBadStatus, PaymentServiceException):
    pass


class PaymentServiceTimeout(ServiceClientTimeout, PaymentServiceBadStatus):
    pass


class PaymentServiceClient(ServiceClientClient):
    GENERAL_EXCEPTION_CLS = PaymentServiceException
    BAD_STATUS_EXCEPTION_CLS = PaymentServiceBadStatus
    TIMEOUT_EXCEPTION_CLS = PaymentServiceTimeout
    SERVICE_NAME = "payment_service"

    class Result(object):
        SUCCESS = "success"
        ERROR_PARAMS = "error_params"
        ERROR_HEADER = "error_header"
        ERROR_SERVER = "error_server"
        ERROR_FORBIDDEN = "error_forbidden"
        ERROR_NOT_FOUND = "error_not_found"

    class Api(object):
        GET_PAYMENT_METHODS = "/s2s/payment/methods"
        PREPAY_VNPAY = "/s2s/vnpay/prepay"
        PREPAY_ZALOPAY = "/s2s/zalopay/prepay"
        PREPAY_MOMO = "/s2s/momo/prepay"
        PREPAY_SHOPEEPAY = "/s2s/shopeepay/prepay"

        REFUND_VNPAY = "/v11/s2s/vnpay/refund"
        REFUND_ZALOPAY = "/v11/s2s/zalopay/refund"
        REFUND_MOMO = "/v11/s2s/momo/refund"
        REFUND_SHOPEEPAY = "/v11/s2s/shopeepay/refund"

        GET_ORDER_TRANSACTIONS_VNPAY = "/s2s/vnpay/get_order_transactions"
        GET_ORDER_TRANSACTIONS_ZALOPAY = "/s2s/zalopay/get_order_transactions"
        GET_ORDER_TRANSACTIONS_MOMO = "/s2s/momo/get_order_transactions"
        GET_ORDER_TRANSACTIONS_SHOPEEPAY = "/s2s/shopeepay/get_order_transactions"


    def get_payment_methods(self, params=None, disable_retry=True):
        return self.request(self.Api.GET_PAYMENT_METHODS, params, method="GET", disable_retry=disable_retry)

    def prepay_vnpay(self, params, disable_retry=True):
        return self.request(self.Api.PREPAY_VNPAY, params, disable_retry=disable_retry)

    def prepay_zalopay(self, params, disable_retry=True):
        return self.request(self.Api.PREPAY_ZALOPAY, params, disable_retry=disable_retry)

    def prepay_momo(self, params, disable_retry=True):
        return self.request(self.Api.PREPAY_MOMO, params, disable_retry=disable_retry)

    def prepay_shopeepay(self, params, disable_retry=True):
        return self.request(self.Api.PREPAY_SHOPEEPAY, params, disable_retry=disable_retry)

    def refund_vnpay(self, params, disable_retry=True):
        return self.request(self.Api.REFUND_VNPAY, params, disable_retry=disable_retry)

    def refund_zalopay(self, params, disable_retry=True):
        return self.request(self.Api.REFUND_ZALOPAY, params, disable_retry=disable_retry)

    def refund_momo(self, params, disable_retry=True):
        return self.request(self.Api.REFUND_MOMO, params, disable_retry=disable_retry)

    def refund_shopeepay(self, params, disable_retry=True):
        return self.request(self.Api.REFUND_SHOPEEPAY, params, disable_retry=disable_retry)

    def get_order_transactions_vnpay(self, params, disable_retry=False):
        return self.request(self.Api.GET_ORDER_TRANSACTIONS_VNPAY, params, disable_retry=disable_retry)

    def get_order_transactions_zalopay(self, params, disable_retry=False):
        return self.request(self.Api.GET_ORDER_TRANSACTIONS_ZALOPAY, params, disable_retry=disable_retry)

    def get_order_transactions_momo(self, params, disable_retry=False):
        return self.request(self.Api.GET_ORDER_TRANSACTIONS_MOMO, params, disable_retry=disable_retry)

    def get_order_transactions_shopeepay(self, params, disable_retry=False):
        return self.request(self.Api.GET_ORDER_TRANSACTIONS_SHOPEEPAY, params, disable_retry=disable_retry)


