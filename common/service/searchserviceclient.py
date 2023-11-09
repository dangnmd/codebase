from common.service.serviceclient import *


class SearchServiceException(ServiceClientException):
    pass


class SearchServiceBadStatus(ServiceClientBadStatus, SearchServiceException):
    pass


class SearchServiceTimeout(ServiceClientTimeout, SearchServiceBadStatus):
    pass


class SearchServiceClient(ServiceClientClient):
    GENERAL_EXCEPTION_CLS = SearchServiceException
    BAD_STATUS_EXCEPTION_CLS = SearchServiceBadStatus
    TIMEOUT_EXCEPTION_CLS = SearchServiceTimeout
    SERVICE_NAME = "search_service"

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
        SEARCH_URL = "/api/search"
        COUNT_URL = "/api/count"
        MORE_LIKE_THIS_URL = "/api/more_like_this"

    def search(self, param):
        return self.request(self.Api.SEARCH_URL, param)

    def count(self, param):
        return self.request(self.Api.COUNT_URL, param)

    def more_like_this(self, param):
        return self.request(self.Api.MORE_LIKE_THIS_URL, param)
