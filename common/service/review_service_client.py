from common.service.serviceclient import *


class ReviewServiceException(ServiceClientException):
    pass


class ReviewServiceBadStatus(ServiceClientBadStatus, ReviewServiceException):
    pass


class ReviewServiceTimeout(ServiceClientTimeout, ReviewServiceBadStatus):
    pass


class ReviewServiceClient(ServiceClientClient):
    GENERAL_EXCEPTION_CLS = ReviewServiceException
    BAD_STATUS_EXCEPTION_CLS = ReviewServiceBadStatus
    TIMEOUT_EXCEPTION_CLS = ReviewServiceTimeout
    SERVICE_NAME = "review_service"

    class Result(object):
        SUCCESS = "success"
        ERROR_PARAMS = "error_params"
        ERROR_HEADER = "error_header"
        ERROR_SERVER = "error_server"
        ERROR_USER_TOKEN = "error_user_token"
        ERROR_SIGNATURE = "error_signature"

    class Api(object):
        HAS_DONE_ON_ORDER = "/s2s/review/has_done_on_order"

    def has_done_on_order(self, param):
        return self.request(self.Api.HAS_DONE_ON_ORDER, param)
