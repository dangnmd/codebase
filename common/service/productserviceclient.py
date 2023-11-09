from common.service.serviceclient import *


class ProductServiceException(ServiceClientException):
    pass


class ProductServiceBadStatus(ServiceClientBadStatus, ProductServiceException):
    pass


class ProductServiceTimeout(ServiceClientTimeout, ProductServiceBadStatus):
    pass


class ProductServiceClient(ServiceClientClient):
    GENERAL_EXCEPTION_CLS = ProductServiceException
    BAD_STATUS_EXCEPTION_CLS = ProductServiceBadStatus
    TIMEOUT_EXCEPTION_CLS = ProductServiceTimeout
    SERVICE_NAME = "product_service"

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
        PRODUCT_GET_INDEX_INFO_BY_LAST_ID_URL = "/s2s/product/get_index_info_by_last_id"
        PRODUCT_GET_INDEX_INFO_BY_IDS_URL = "/s2s/product/get_index_info_by_ids"
        PRODUCT_CLEAR_CACHE_URL = "/s2s/clear_cache"
        PRODUCT_REWRITE_GET_INFO_URL = "/s2s/rewrite_url/get_info"
        PRODUCT_GET_DETAIL_BY_SELLER_URL = "/s2s/product/get_detail_by_seller"
        PRODUCT_VALIDATE_URL = "/s2s/product/validate"
        SELLER_GET_INFO_URL = "/s2s/seller/get_infos"
        SELLER_GET_PRODUCT_KIND_INFOS_URL = "/s2s/seller/get_product_kind_infos"
        CATEGORY_GET_INFO_URL = "/s2s/category/get_infos"
        SUB_CATEGORY_GET_INFO_URL = "/s2s/sub_category/get_infos"
        BRAND_GET_INFO_URL = "/s2s/seller/get_product_brand_infos"
        CITY_GET_INFO_URL = "/s2s/city/get_infos"
        PRODUCT_GET_PROCEEDINGS = "/s2s/product/get_proceedings"
        PRODUCT_GET_CATEGORIES = "/s2s/product/get_categories"
        PRODUCT_GET_SUB_CATEGORIES = "/s2s/product/get_sub_categories"

    def get_index_info_by_last_id(self, params):
        return self.request(self.Api.PRODUCT_GET_INDEX_INFO_BY_LAST_ID_URL, params)

    def get_index_info_by_ids(self, params):
        return self.request(self.Api.PRODUCT_GET_INDEX_INFO_BY_IDS_URL, params)

    def clear_cache(self, params):
        return self.request(self.Api.PRODUCT_CLEAR_CACHE_URL, params)

    def rewrite_get_info(self, params):
        return self.request(self.Api.PRODUCT_REWRITE_GET_INFO_URL, params)

    def get_detail_by_seller(self, params):
        return self.request(self.Api.PRODUCT_GET_DETAIL_BY_SELLER_URL, params)

    def get_seller_infos(self, params):
        return self.request(self.Api.SELLER_GET_INFO_URL, params)

    def get_product_kind_infos(self, params):
        return self.request(self.Api.SELLER_GET_PRODUCT_KIND_INFOS_URL, params)

    def get_category_infos(self, params):
        return self.request(self.Api.CATEGORY_GET_INFO_URL, params)

    def get_brand_infos(self, params):
        return self.request(self.Api.BRAND_GET_INFO_URL, params)

    def get_city_infos(self, params):
        return self.request(self.Api.CITY_GET_INFO_URL, params)

    def validate(self, params):
        return self.request(self.Api.PRODUCT_VALIDATE_URL, params, method="POST")

    def get_subcategory_infos(self, params):
        return self.request(self.Api.SUB_CATEGORY_GET_INFO_URL, params)
    
    def get_proceedings(self, params):
        return self.request(self.Api.PRODUCT_GET_PROCEEDINGS, params)

    def get_categories(self, params):
        return self.request(self.Api.PRODUCT_GET_CATEGORIES, params)

    def get_sub_categories(self, params):
        return self.request(self.Api.PRODUCT_GET_SUB_CATEGORIES, params)

