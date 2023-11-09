from common.service.serviceclient import *


class AppServiceException(ServiceClientException):
    pass


class AppServiceBadStatus(ServiceClientBadStatus, AppServiceException):
    pass


class AppServiceTimeout(ServiceClientTimeout, AppServiceBadStatus):
    pass


class AppServiceClient(ServiceClientClient):
    GENERAL_EXCEPTION_CLS = AppServiceException
    BAD_STATUS_EXCEPTION_CLS = AppServiceBadStatus
    TIMEOUT_EXCEPTION_CLS = AppServiceTimeout
    SERVICE_NAME = "app_service"

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

    class Api(object):
        ROUTE_GET_URLS = "/s2s/route/get_urls"

    def get_urls(self, params):
        return self.request(self.Api.ROUTE_GET_URLS, params)
