from common.service.serviceclient import *


class MePosServiceException(ServiceClientException):
    pass


class MePosServiceBadStatus(ServiceClientBadStatus, MePosServiceException):
    pass


class MePosServiceTimeout(ServiceClientTimeout, MePosServiceBadStatus):
    pass


class MePosServiceClient(ServiceClientClient):
    GENERAL_EXCEPTION_CLS = MePosServiceException
    BAD_STATUS_EXCEPTION_CLS = MePosServiceBadStatus
    TIMEOUT_EXCEPTION_CLS = MePosServiceTimeout
    SERVICE_NAME = "mepos_service"

    class Result(object):
        SUCCESS = "success"
        ERROR_PARAMS = "error_params"
        ERROR_HEADER = "error_header"
        ERROR_SERVER = "error_server"
        ERROR_FORBIDDEN = "error_forbidden"
        ERROR_DATA_NOT_EXISTS = "error_data_not_exists"

    class Api(object):
        GET_NEAREST_LOCATION = "/s2s/seller/get_info_by_distance"

    def get_nearest_location(self, params):
        return self.request(self.Api.GET_NEAREST_LOCATION, params)
