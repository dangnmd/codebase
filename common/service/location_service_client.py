from common.service.serviceclient import *


class LocationServiceException(ServiceClientException):
    pass


class LocationServiceBadStatus(ServiceClientBadStatus, LocationServiceException):
    pass


class LocationServiceTimeout(ServiceClientTimeout, LocationServiceBadStatus):
    pass


class LocationServiceClient(ServiceClientClient):
    GENERAL_EXCEPTION_CLS = LocationServiceException
    BAD_STATUS_EXCEPTION_CLS = LocationServiceBadStatus
    TIMEOUT_EXCEPTION_CLS = LocationServiceTimeout
    SERVICE_NAME = "location_service"

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
        ERROR_ORIGIN_NOT_ALLOW = "error_origin_not_allow"
        ERROR_KEY_NOT_FOUND = "error_key_not_found"
        ERROR_INVALID_LAT_LNG = "error_invalid_lat_lng"

    class Api(object):
        GET_DISTANCE = "/api/distance/get_distance"
        GET_CITY = "/api/city/detect_city"

    def get_distance(self, params):
        return self.request(self.Api.GET_DISTANCE, params)

    def get_city(self, params):
        return self.request(self.Api.GET_CITY, params)
