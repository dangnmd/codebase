import random
import requests
from .logger import log
from .jsonutils import to_json

class FApiServiceBadStatus(Exception):
	def __init__(self, request_id, http_status):
		self.request_id = request_id
		self.http_status = http_status

	def __str__(self):
		return "%s - %s" % (self.request_id, self.http_status)

class FApiServiceTimeout(Exception):
	def __init__(self, request_id):
		self.request_id = request_id

	def __str__(self):
		return str(self.request_id)

class FApiServiceClient(object):
	APP_VERSION = "1"
	UPDATE_STATUS_TIMEOUT = 15

	class Result(object):
		SUCCESS = "success"
		ERROR_HEADER = "error_header"
		ERROR_PARAMS = "error_params"
		ERROR_SERVER = "error_server"
		ERROR_FORBIDDEN = "error_forbidden"
		ERROR_NOT_IN_WHITE_LIST = "error_not_in_whitelist"
		ERROR_NO_HR_EMPLOYEE = 'error_no_hr_employee'
		ERROR_NO_HR_CONTACT = 'error_no_hr_contact'
		ERROR_SIGNATURE = "error_signature"
		ERROR_ACCOUNT_INVALID = "error_account_invalid"
		ERROR_URL_NOT_EXIST = "error_url_not_exist"
		ERROR_URL_CODE_EXIST = "error_url_code_exist"
		ERROR_URL_EXIST = "error_url_exist"
		ERROR_ACCOUNT_NOT_EXIST = "error_account_not_exist"
		ERROR_TEMPLATE_NOT_EXIST = "error_template_not_exist"
		ERROR_UPDATE_ORDER_STATUS = 'error_update_order_status'
		ERROR_ORDER_NOT_EXIST = 'error_order_not_exist'
		ERROR_EMAIL_EXISTED = 'error_email_existed'
		ERROR_USERNAME_EXISTED = 'error_username_existed'

	class Api(object):
		ADMIN_SEARCH_ORDER = "/admin/order/search"
		ADMIN_ORDER_GET_CC_BOOKING_BY_SHIPPER_UIDS = '/admin/order/get_cc_booking_by_shipper_uids'
		ADMIN_ORDER_CREATE_CC_BOOKINGS = '/admin/order/create_cc_bookings'

		ADMIN_ONMAP_GET_SHIPPER_UIDS = '/admin/onmap/get_shipper_uids'
		ADMIN_ONMAP_GET_SHIPPER_INFOS = '/admin/onmap/get_shipper_infos'
		ADMIN_ONMAP_GET_CC_SHIPPER_NOTES = '/admin/onmap/get_cc_shipper_notes'
		ADMIN_ONMAP_CREATE_CC_SHIPPER_NOTE = '/admin/onmap/create_cc_shipper_note'

		ADVANCE_PAYMENT_CREATE_SHIPPER_PAYMENT = "/shipper/advance_payment/create_shipper_payment"
		ADVANCE_PAYMENT_GET_SHIPPER_PAYMENTS_BY_CITY_ID = "/shipper/advance_payment/get_shipper_payments_by_city_id"
		ADVANCE_PAYMENT_GET_SHIPPER_STATS_BY_MONTH = "/shipper/advance_payment/get_shipper_stats_by_month"
		ADVANCE_PAYMENT_UPDATE_SHIPPER_PAYMENT = "/shipper/advance_payment/update_shipper_payment"

		AIRPAY_CREATE_TRANSACTION_LOG = '/airpay/create_transaction_log'
		AIRPAY_GET_MERCHANT_BY_STORE_IDS = '/airpay/get_merchant_by_store_ids'
		AIRPAY_GET_STORE_ID_BY_RESTAURANT = '/airpay/get_store_id_by_restaurant_ids'
		AIRPAY_GET_TRANSACTION_LOGS = '/airpay/get_transaction_logs'
		AIRPAY_POST_PAYMENT = '/airpay/post_payment'

		APP_GET_DETAILS = "/app/get_details"

		BLACK_LIST_CHECK_PAYMENT_UIDS = '/black_list/check_payment_uids'
		BLACK_LIST_CHECK_UIDS = '/black_list/check_uids'

		BRAND_GET_BASIC_INFO = '/brand/get_basic_info'
		BRAND_GET_IDS = '/brand/get_ids'

		CAMPAIGN_GET_AVAILABLE_CAMPAIGNS = "/campaign/get_available_campaigns"
		CAMPAIGN_GET_CAMPAIGNS_BY_IDS = "/campaign/get_campaigns_by_ids"
		CAMPAIGN_GET_DELIVERY_VALID_CAMPAIGNS = "/campaign/get_delivery_valid_campaigns"
		CAMPAIGN_GET_TYPES = "/campaign/get_types"

		COLLECTION_GET_BASIC_INFOS = '/collection/get_basic_infos'
		COLLECTION_GET_IDS_BY_DELIVERY_CATEGORY_IDS = '/collection/get_ids_by_delivery_category_ids'
		COLLECTION_GET_ITEMS_BY_COLLECTION_IDS = '/collection/item/get_infos_by_collection_ids'

		COMMISSION_GET_INFOS = '/commission/get_infos'
		COMMISSION_GET_INFOS_BY_DELIVERY = '/commission/get_infos_by_delivery'
		COMMISSION_GET_TYPES = '/commission/get_types'
		COMMISSION_UPDATE_CS_BY_ORDER = '/commission/update_cs_by_order'

		CONVERSATION_COUNT_MESSAGE = '/conversation/count_message'
		CONVERSATION_CREATE_MESSAGE = '/conversation/create_message'
		CONVERSATION_GET_MESSAGES = '/conversation/get_messages'
		CONVERSATION_GET_MESSAGE_BY_IDS = '/conversation/get_message_by_ids'
		CONVERSATION_GET_MESSAGE_TEMPLATES_BY_TYPES = '/conversation/get_message_templates_by_types'
		CONVERSATION_GET_OR_CREATE = '/conversation/get_or_create'
		CONVERSATION_GET_UIDS = '/conversation/get_uids'
		CONVERSATION_MARK_SEEN_MESSAGES = '/conversation/mark_seen_messages'
		CONVERSATION_UPDATE_MESSAGE = '/conversation/update_message'

		DELIVERY_CREATE_BUSY = '/delivery/create_busy'
		DELIVERY_GET_BASIC_INFOS = "/delivery/get_basic_infos"
		DELIVERY_GET_BUSY_INFO_BY_CITY_ID = '/delivery/get_busy_info_by_city_id'
		DELIVERY_GET_BUSY_INFO_BY_DELIVERY_ID = '/delivery/get_busy_info_by_delivery_id'
		DELIVERY_GET_DETAIL = "/delivery/get_detail"
		DELIVERY_GET_EMPLOYEE_UIDS = "/delivery/get_employee_uids"
		DELIVERY_GET_IDS_BY_CATEGORY_IDS = "/delivery/get_ids_by_category_ids"
		DELIVERY_GET_IDS_BY_OWNER_UID = "/delivery/get_ids_by_owner_uid"
		DELIVERY_GET_IDS_BY_RESTAURANT_IDS = "/delivery/get_ids_by_restaurant_ids"
		DELIVERY_GET_IDS_BY_UID = "/delivery/get_ids_by_uid"
		DELIVERY_GET_OPENNING_IDS = "/delivery/get_openning_ids"
		DELIVERY_GET_RECENT_IDS = "/delivery/get_recent_ids"
		DELIVERY_GET_RELATED_IDS = "/delivery/get_related_ids"
		DELIVERY_GET_SUBSCRIBE_IDS = "/delivery/get_subscribe_ids"
		DELIVERY_GET_SUCCESSFUL_ORDERED_IDS = "/delivery/get_successful_ordered_ids"
		DELIVERY_GET_TIME_RANGES = '/delivery/get_time_ranges'
		DELIVERY_SET_TIME_RANGE = '/delivery/set_time_range'
		DELIVERY_UPDATE = "/delivery/update"
		DELIVERY_UPDATE_BUSY_BY_DELIVERY_ID = '/delivery/update_busy_by_delivery_id'

		DELIVERY_CATEGORY_CREATE = "/delivery/category/create"
		DELIVERY_CATEGORY_CREATE_MAPPING = "/delivery/category/create_mapping"
		DELIVERY_CATEGORY_DELETE = "/delivery/category/delete"
		DELIVERY_CATEGORY_DELETE_MAPPING = "/delivery/category/delete_mapping"
		DELIVERY_CATEGORY_GET_IDS_BY_COUNTRY_ID = "/delivery/category/get_ids_by_country_id"
		DELIVERY_CATEGORY_GET_IDS_BY_DELIVERY_IDS = "/delivery/category/get_ids_by_delivery_ids"
		DELIVERY_CATEGORY_GET_IDS_BY_FOODY_SERVICE_IDS = "/delivery/category/get_ids_by_foody_service_ids"
		DELIVERY_CATEGORY_GET_IDS_BY_PARENT_IDS = "/delivery/category/get_ids_by_parent_ids"
		DELIVERY_CATEGORY_GET_INFO = "/delivery/category/get_infos"
		DELIVERY_CATEGORY_UPDATE = "/delivery/category/update"

		DELIVERY_ADDRESS_CREATE = "/delivery_address/create"
		DELIVERY_ADDRESS_DELETE = "/delivery_address/delete"
		DELIVERY_ADDRESS_GET_DETAILS = "/delivery_address/get_details"
		DELIVERY_ADDRESS_GET_DETAILS_BY_SHIPPING_ID = "/delivery_address/get_details_by_shipping_id"
		DELIVERY_ADDRESS_GET_IDS = "/delivery_address/get_ids"
		DELIVERY_ADDRESS_UPDATE = "/delivery_address/update"

		DISH_CHECK_AVAILABLE = '/dish/check_available'
		DISH_COUNT_OUT_OF_DISH = '/dish/count_out_of_dish'
		DISH_CREATE_OUT_OF_DISH = "/dish/create_out_of_dish"
		DISH_CREATE_SCHEDULED_QUANTITY = '/dish/create_scheduled_quantity'
		DISH_GET_IDS_BY_RESTAURANT_ID = '/dish/get_ids_by_restaurant_id'
		DISH_GET_INFOS = '/dish/get_infos'
		DISH_GET_OUT_OF_DISH = "/dish/get_out_of_dish"
		DISH_GET_PRICES = '/dish/get_prices'
		DISH_GET_SCHEDULED_QUANTITY = '/dish/get_scheduled_quantity'
		DISH_GET_SHEIS_PRODUCT_IDS = '/dish/get_sheis_product_ids'
		DISH_GET_TIME_RANGES = '/dish/get_time_ranges'
		DISH_MARK_AS_OUT_OF_DISH = '/dish/mark_as_out_of_dish'
		DISH_UPDATE_ACTIVE = '/dish/update_active'
		DISH_UPDATE_OUT_OF_DISH = "/dish/update_out_of_dish"
		DISH_UPDATE_SCHEDULED_QUANTITY = '/dish/update_scheduled_quantity'

		DISH_OPTION_GET_DETAILS_BY_DISH_IDS = '/dish/option/get_details_by_dish_ids'
		DISH_OPTION_GET_INFOS = '/dish/option/get_infos'
		DISH_OPTION_GET_ITEMS = '/dish/option/get_items'
		DISH_OPTION_GET_ITEM_MAPPING_BY_DISH_IDS = '/dish/option/get_item_mapping_by_dish_ids'

		DISH_TYPE_GET_IDS_BY_DISH_IDS = '/dish/type/get_ids_by_dish_ids'
		DISH_TYPE_GET_INFOS = '/dish/type/get_infos'
		DISH_TYPE_GET_INFO_BY_RESTAURANT_ID = '/dish/type/get_infos_by_restaurant_id'

		FEEDBACK_CREATE_MERCHANT_FEEDBACK = '/feedback/create_merchant_feedback'
		FEEDBACK_CREATE_USER_FEEDBACK = '/feedback/create_user_feedback'
		FEEDBACK_UPLOAD_IMG_FEEDBACK = '/feedback/create_user_feedback_photo'
		FEEDBACK_GET_CC_FEEDBACK_MERCHANT_PROPERTIES = '/feedback/get_cc_feedback_merchant_properties'
		FEEDBACK_GET_CC_FEEDBACKS_MERCHANT = '/feedback/get_cc_feedbacks_merchant'
		FEEDBACK_CREATE_CC_FEEDBACK_MERCHANT = '/feedback/create_cc_feedback_merchant'
		FEEDBACK_DELETE_CC_FEEDBACKS_MERCHANT = '/feedback/delete_cc_feedbacks_merchant'
		FEEDBACK_GET_OPTIONS_BY_TYPES = '/feedback/get_options_by_types'
		FEEDBACK_CREATE_CC_SHIPPER_FEEDBACK = '/feedback/create_cc_shipper_feedback'
		FEEDBACK_GET_CC_SHIPPER_FEEDBACKS = '/feedback/get_cc_shipper_feedbacks'
		FEEDBACK_UPDATE_CC_SHIPPER_FEEDBACK = '/feedback/update_cc_shipper_feedback'

		FLOOR_GET_INFOS = '/floor/get_infos'

		HUB_GET_INFOS_BY_CITY_ID = '/hub/get_infos_by_city_id'

		INVOICE_ADDRESS_GET_ORDER_ADDRESS_BY_IDS = '/invoice_address/get_order_address_by_ids'
		INVOICE_ADDRESS_CREATE = '/invoice_address/create'
		INVOICE_ADDRESS_CREATE_ORDER_ADDRESS = '/invoice_address/create_order_address'
		INVOICE_ADDRESS_DELETE = '/invoice_address/delete'
		INVOICE_ADDRESS_DELETE_ORDER_ADDRESS = '/invoice_address/delete_order_address'
		INVOICE_ADDRESS_GET_BY_ORDER_IDS = '/invoice_address/get_by_order_ids'
		INVOICE_ADDRESS_GET_BY_UID = '/invoice_address/get_by_uid'
		INVOICE_ADDRESS_GET_INFOS = '/invoice_address/get_infos'
		INVOICE_ADDRESS_UPDATE = '/invoice_address/update'
		INVOICE_ADDRESS_UPDATE_BY_ORDER_ID = '/invoice_address/update_by_order_id'

		LOCATION_GET_COUNTRIES = "/location/get_countries"
		LOCATION_GET_DISTRICTS = "/location/get_districts"
		LOCATION_GET_DISTRICTS_BY_PROVINCE = "/location/get_districts_by_province"
		LOCATION_GET_PROVINCES = "/location/get_provinces"
		LOCATION_GET_PROVINCES_BY_COUNTRY = "/location/get_provinces_by_country"

		LOG_CREATE_CHANGE_LOG = '/log/create_change_log'
		LOG_CREATE_CHECKIN_CHECKOUT = '/log/create_checkin_checkout'
		LOG_CREATE_SHIPPER_ACTION_LOGS = '/log/create_shipper_action_logs'
		LOG_CREATE_SHIPPER_LOCATION = '/log/create_shipper_location'
		LOG_GET_LATEST_CHECKIN_CHECKOUT_INFO = '/log/get_latest_checkin_checkout_info'
		LOG_SET_REPORT_DEPOSIT = '/log/set_report_deposit'
		LOG_UPDATE_CHECKIN_CHECKOUT = '/log/update_checkin_checkout'
		LOG_UPDATE_SHIPPER_ACTION_LOGS = '/log/update_shipper_action_logs'

		MAIL_GET_ACCOUNT = '/mail/get_account'
		MAIL_GET_ACCOUNTS = '/mail/get_accounts'
		MAIL_GET_TEMPLATE = '/mail/get_template'
		MAIL_GET_TEMPLATES = '/mail/get_templates'
		MAIL_SEND = '/mail/send'
		MAIL_SEND_MANY = '/mail/send_many'

		MERCHANT_CATEGORY_GET_BY_DELIVERY_IDS = '/merchant_category/get_by_delivery_ids'

		ORDER_CHANGE_DELIVERY = '/order/change_delivery'
		ORDER_CHANGE_UID = '/order/change_uid'
		ORDER_CLONE_COMPLETED_ORDER = '/order/clone_completed_order'
		ORDER_CHANGE_SHIPPING_INFO = '/order/change_shipping_info'
		ORDER_COUNT_PAID_BY_CARD_ORDER = '/order/count_paid_by_card_order'
		ORDER_COUNT_BY_SHIPPING_INFO_IDS = '/order/count_by_shipping_info_ids'
		ORDER_CREATE_ATTRIBUTE = '/order/attribute/create'
		ORDER_CREATE_DELIVERY_ORDER_IMAGE = '/order/create_delivery_order_image'
		ORDER_CREATE_DISCOUNT = '/order/create_discount'
		ORDER_CREATE_DISCOUNTS = '/order/create_discounts'
		ORDER_CREATE_FEEDBACK = '/order/create_feedback'
		ORDER_CREATE_MANY_ATTRIBUTES = '/order/attribute/create_many'
		ORDER_CREATE_ORDER_IMAGE = '/order/image/create'
		ORDER_CREATE_TIP = '/order/tip/create'
		ORDER_DELETE_DISCOUNT_BY_ORDER_ID = '/order/delete_discount_by_order_id'
		ORDER_GET_ADDITIONAL_FEES = '/order/get_additional_fees'
		ORDER_GET_ATTRIBUTES = '/order/attribute/get_infos'
		ORDER_GET_BASIC_INFOS = '/order/get_basic_infos'
		ORDER_GET_BASIC_INFOS_BY_CODES = '/order/get_basic_infos_by_codes'
		ORDER_GET_CUSTOMER_RATINGS = '/order/get_customer_ratings'
		ORDER_GET_DISCOUNT_INFOS = '/order/get_discount_infos'
		ORDER_GET_EXTENDED_INFOS = '/order/get_extended_infos'
		ORDER_GET_FREE_PICK_ORDERS_IN_RANGE = '/order/get_free_pick_in_range'
		ORDER_GET_IDS_BY_UID = '/order/get_ids_by_uid'
		ORDER_GET_NOTE_BY_IDS = '/order/get_note_by_ids'
		ORDER_GET_NOTE_BY_TYPE = '/order/get_note_by_type'
		ORDER_GET_PROCESSING_IDS_BY_UID = '/order/get_processing_ids_by_uid'
		ORDER_GET_TIP_AMOUNT = '/order/tip/get_amount'
		ORDER_GET_USER_RECENT_IDS = '/order/get_user_recent_ids'
		ORDER_GET_WARRANTY_TRANSACTIONS_BY_ORDER_IDS = '/order/get_warranty_transactions_by_order_ids'
		ORDER_SEARCH = '/order/search'
		ORDER_SET_ORDER_ALERT_CONFIRM = '/order/set_order_alert_confirm'
		ORDER_SUBMIT = '/order/submit'
		ORDER_UPDATE = '/order/update'
		ORDER_UPDATE_ATTRIBUTE = '/order/attribute/update'
		ORDER_UPDATE_EXTENDED_INFO = '/order/update_extended_info'
		ORDER_UPDATE_MANY_ATTRIBUTES = '/order/attribute/update_many'
		ORDER_UPDATE_STATUS = '/order/update_status'

		ORDER_CREATE_ITEM = '/order/item/create'
		ORDER_CREATE_MANY_ITEMS = '/order/item/create_many'
		ORDER_GET_ITEM_INFOS_BY_ORDER_IDS = '/order/item/get_infos_by_order_ids'
		ORDER_UPDATE_ITEM = '/order/item/update'
		ORDER_UPDATE_MANY_ITEMS = '/order/item/update_many'

		ORDER_CREATE_LOG = '/order/log/create'
		ORDER_CREATE_MANY_LOGS = '/order/log/create_many'
		ORDER_CREATE_MERCHANT_LOG = '/order/log/create_merchant_log'
		ORDER_CREATE_STATUS_LOG = '/order/log/create_status'
		ORDER_GET_STATUS_LOGS = '/order/log/get_statuses'

		ORDER_CREATE_SMS_MESSAGES = '/order/message/create_sms'
		ORDER_GET_SMS_MESSAGES = '/order/message/get_sms'

		PAYMENT_GET_MERCHANT_PAY_STATUSES = '/payment/get_merchant_pay_statuses'
		PAYMENT_GET_MERCHANT_PAY_TYPES = '/payment/get_merchant_pay_types'
		PAYMENT_GET_METHODS = '/payment/get_methods'
		PAYMENT_GET_METHOD_APP_TYPE_MAPPINGS = '/payment/get_method_app_type_mappings'
		PAYMENT_GET_METHOD_SERVICE_MAPPINGS = '/payment/get_method_service_mappings'
		PAYMENT_GET_ORDER_CARD_INFO = '/payment/get_order_card_info'

		PAYNOW_CREATE_BALANCE = '/paynow/create_balance'
		PAYNOW_CREATE_TRANSACTION = '/paynow/create_transaction'
		PAYNOW_GET_BALANCES = '/paynow/get_balances'
		PAYNOW_GET_TRANSACTIONS = '/paynow/get_transactions'

		PUSH_COUNT_MESSAGE = '/push/count_message'
		PUSH_GET_MESSAGES = '/push/get_messages'
		PUSH_GET_NEWS = '/push/get_news'
		PUSH_MARK_ALL_MESSAGE_SEEN = '/push/mark_all_messages_seen'
		PUSH_MARK_MESSAGE_SEEN = '/push/mark_messages_seen'
		PUSH_REGISTER_DEVICE_TOKEN = '/push/register_device_token'
		PUSH_UNREGISTER_DEVICE_TOKEN = '/push/unregister_device_token'

		PROMOTION_APPLY_PROMO_CODE = "/promotion/apply_promo_code"
		PROMOTION_CREATE_MERCHANT_DISCOUNT_REQUEST = '/promotion/create_merchant_discount_request'
		PROMOTION_GET_DISH_OFFERS = "/promotion/get_dish_offers"
		PROMOTION_GET_NEWS = "/promotion/get_news"
		PROMOTION_GET_OFFERS = "/promotion/get_offers"
		PROMOTION_GET_OFFERS_BY_DELIVERY_ID = "/promotion/get_offers_by_delivery_id"
		PROMOTION_GET_OFFERS_BY_STATUS = "/promotion/get_offers_by_status"
		PROMOTION_GET_PROMO_CODES = "/promotion/get_promo_codes"
		PROMOTION_GET_PROMO_CODES_BY_CODE = "/promotion/get_promo_codes_by_code"
		PROMOTION_GET_PROMO_CODE_APPLY_CONDITIONS = "/promotion/get_promo_code_apply_conditions"
		PROMOTION_GET_PROMO_CODE_TOTAL_USED = "/promotion/get_promo_code_total_used"
		PROMOTION_REMOVE_PROMO_CODE = "/promotion/remove_promo_code"
		PROMOTION_VALIDATE_CORPORATE_GROUP = "/promotion/validate_corporate_group"
		PROMOTION_VALIDATE_DELIVER_DATETIME = "/promotion/validate_deliver_datetime"
		PROMOTION_VALIDATE_PAYMENT_METHOD = "/promotion/validate_payment_method"
		PROMOTION_VALIDATE_PERSONAL = "/promotion/validate_personal"
		PROMOTION_VALIDATE_RESTAURANT = "/promotion/validate_restaurant"
		PROMOTION_VALIDATE_RESTAURANT_LOCATION = "/promotion/validate_restaurant_location"
		PROMOTION_VALIDATE_ROOT_CATEGORY = "/promotion/validate_root_category"
		PROMOTION_VALIDATE_SHIPPING_METHOD = "/promotion/validate_shipping_method"
		PROMOTION_VALIDATE_TOTAL_ORDER_DELIVERED = "/promotion/validate_total_order_delivered"

		REPORT_GET_ORDER_DEPOSIT = '/report/get_order_deposit'
		REPORT_SET_ORDER_DEPOSIT = '/report/set_order_deposit'

		RESTAURANT_CREATE_FAVORITE = "/restaurant/create_favorite"
		RESTAURANT_DELETE = "/restaurant/delete"
		RESTAURANT_DELETE_FAVORITE = "/restaurant/delete_favorite"
		RESTAURANT_GET_BASIC_INFOS = "/restaurant/get_basic_infos"
		RESTAURANT_GET_FAVORITE_IDS = "/restaurant/get_favorite_ids"
		RESTAURANT_GET_IDS_BY_BRAND = "/restaurant/get_ids_by_brand"
		RESTAURANT_GET_IDS_BY_CITY = "/restaurant/get_ids_by_city"
		RESTAURANT_GET_IDS_BY_DELIVERY_IDS = "/restaurant/get_ids_by_delivery_ids"
		RESTAURANT_GET_PHONES = "/restaurant/get_phones"
		RESTAURANT_GET_STATS = "/restaurant/get_stats"
		RESTAURANT_SEARCH_IDS_BY_NAME = "/restaurant/search_ids_by_name"
		RESTAURANT_SUBSCRIBE = "/restaurant/subscribe"
		RESTAURANT_UNSUBSCRIBE = "/restaurant/unsubscribe"
		RESTAURANT_UPDATE = "/restaurant/update"

		RESTAURANT_CATEGORY_GET_IDS_BY_RESTAURANT_IDS = "/restaurant/category/get_ids_by_restaurant_ids"
		RESTAURANT_CATEGORY_GET_INFOS = "/restaurant/category/get_infos"

		RESTAURANT_CUISINE_GET_BY_CATEGORY_IDS = "/restaurant/cuisine/get_ids_by_category_ids"
		RESTAURANT_CUISINE_GET_IDS_BY_RESTAURANT_IDS = "/restaurant/cuisine/get_ids_by_restaurant_ids"
		RESTAURANT_CUISINE_GET_INFOS = "/restaurant/cuisine/get_infos"

		RUSH_HOUR_GET_INFOS = "/rush_hour/get_infos"
		RUSH_HOUR_GET_TYPES = "/rush_hour/get_types"

		SETTING_GET_CONFIRM_METHOD_IDS_BY_CITY_IDS = "/setting/get_confirmation_method_ids_by_city_ids"
		SETTING_GET_CONFIRM_METHOD_SETTINGS = "/setting/get_confirmation_method_settings"
		SETTING_GET_FOODY_GENERAL_SETTINGS = "/setting/get_foody_general_settings"
		SETTING_GET_FOODY_SERVICES = '/setting/get_foody_services'
		SETTING_GET_GENERAL_SETTINGS = "/setting/get_general_settings"
		SETTING_GET_GOOGLE_API_KEYS = "/setting/get_google_api_keys"
		SETTING_GET_HOME_MESSAGE = "/setting/get_home_message"
		SETTING_GET_GET_METADATA_SETTINGS = "/setting/get_metadata_settings"
		SETTING_GET_ORDER_STATUS_SETTINGS = "/setting/get_order_status_settings"
		SETTING_GET_PRINTER_SETTINGS = "/setting/get_printer_settings"
		SETTING_GET_TIME_RANGE_SETTING = "/setting/get_time_range_setting"
		SETTING_GET_ZONE_SETTING = "/setting/get_zone_setting"
		SETTING_SET_GENERAL_SETTING = "/setting/set_general_setting"
		SETTING_GET_HOME_FILTER = "/setting/get_home_filter"
		SETTING_GET_HOME_FILTER_BY_FOODY_SERVICE_IDS = "/setting/get_home_filter_by_foody_service_ids"
		SETTING_GET_FOODY_SERVICE_BY_CITY_IDS = '/setting/get_foody_service_by_city_ids'
		SETTING_SEARCH_GENERAL_SETTINGS = "/setting/search_general_settings"
		SETTING_SEARCH_ZONE_SETTINGS = "/setting/search_zone_settings"
		SETTING_SET_ZONE_SETTING = "/setting/set_zone_setting"

		SHIFT_GET_INFOS = '/shipper/shift/get_infos'
		SHIFT_GET_INFOS_BY_CITY_ID = '/shipper/shift/get_infos_by_city_id'
		SHIFT_GET_SHIPPER_OFF_INFOS = '/shipper/shift/get_shipper_off_infos'
		SHIFT_GET_SHIPPER_OFF_INFOS_BY_CITY_ID = '/shipper/shift/get_shipper_off_infos_by_city_id'
		SHIFT_GET_SHIPPER_ONSHIFT_INFOS = '/shipper/shift/get_shipper_onshift_infos'
		SHIFT_GET_SHIPPER_ONSHIFT_INFOS_BY_CITY_ID = '/shipper/shift/get_shipper_onshift_infos_by_city_id'
		SHIFT_GET_USER_REGISTERED = '/shipper/shift/get_user_registered'

		SHIPPER_VIOLATION_CREATE = '/shipper/violation/create'
		SHIPPER_VIOLATION_CREATE_TYPE = '/shipper/violation/create_type'
		SHIPPER_VIOLATION_GET_SHIPPER_INFOS = '/shipper/violation/get_shipper_infos'
		SHIPPER_VIOLATION_UPDATE = '/shipper/violation/update'
		SHIPPER_VIOLATION_UPDATE_TYPE = '/shipper/violation/update_type'

		SHIPPING_CREATE = '/shipping/create'
		SHIPPING_GET_IDS = '/shipping/get_ids'
		SHIPPING_GET_IDS_BY_ADDRESS_ID = '/shipping/get_ids_by_address_ids'
		SHIPPING_GET_IDS_BY_PHONE = '/shipping/get_ids_by_phone'
		SHIPPING_GET_INFOS = '/shipping/get_infos'
		SHIPPING_GET_LAST_INFO_BY_UID = '/shipping/get_last_info_by_uid'
		SHIPPING_GET_METHODS = '/shipping/get_methods'
		SHIPPING_GET_METHOD_DETAIL_BY_DELIVERY = '/shipping/get_method_detail_by_delivery'
		SHIPPING_GET_METHOD_IDS_BY_DELIVERY = '/shipping/get_method_ids_by_delivery'
		SHIPPING_GET_MILESTONE_TIME = '/shipping/get_milestone_time'
		SHIPPING_GET_RECENT_IDS = '/shipping/get_recent_ids'
		SHIPPING_UPDATE = '/shipping/update'
		SHIPPING_UPDATE_VERIFIED = '/shipping/update_verified'

		SHOPPING_CART_ADD_LOG = '/shopping_cart/add_log'
		SHOPPING_CART_CREATE = '/shopping_cart/create'
		SHOPPING_CART_DELETE = '/shopping_cart/delete'
		SHOPPING_CART_DELETE_BY_UID = '/shopping_cart/delete_by_uid'
		SHOPPING_CART_DELETE_USER_ORDER_IN_GROUP = '/shopping_cart/delete_user_order_in_group'
		SHOPPING_CART_GET_INFOS = '/shopping_cart/get_infos'
		SHOPPING_CART_GET_LOG = '/shopping_cart/get_log'
		SHOPPING_CART_REFRESH_PRICE = '/shopping_cart/refresh_price'
		SHOPPING_CART_SET_GROUP_CART_VERSION = '/shopping_cart/set_group_cart_version'
		SHOPPING_CART_UPDATE = '/shopping_cart/update'
		SHOPPING_CART_UPDATE_CART_ORDER_LOG = '/shopping_cart/update_log'

		SHOPPING_CART_CREATE_ITEMS = '/shopping_cart/item/create'
		SHOPPING_CART_DELETE_ITEMS = '/shopping_cart/item/delete'
		SHOPPING_CART_DELETE_ITEMS_BY_CART_ID = '/shopping_cart/item/delete_by_cart_id'
		SHOPPING_CART_GET_ITEM_BY_UID = '/shopping_cart/item/get_by_uid'
		SHOPPING_CART_GET_ITEM_INFOS = '/shopping_cart/item/get_infos'
		SHOPPING_CART_UPDATE_ITEM = '/shopping_cart/item/update'
		SHOPPING_CART_UPDATE_ITEM_DONE = '/shopping_cart/item/update_done'

		SOS_CREATE = '/sos/create'
		SOS_DELETE = '/sos/delete'
		SOS_GET_INFO_BY_UID = '/sos/get_info_by_uid'
		SOS_GET_TYPES = '/sos/get_types'

		STATS_GET_DELIVERY_STATS_BY_CITY = '/stats/get_delivery_stats_by_city'
		STATS_GET_ORDER_STATS_BY_PHONES = '/stats/get_order_stats_by_phones'
		STATS_GET_ORDER_STATS_BY_SHIPPING_INFO_IDS = '/stats/get_order_stats_by_shipping_info_ids'

		TRANSACTION_GET_INFOS = '/transaction/get_infos'
		TRANSACTION_GET_INFOS_BY_ORDER_IDS = '/transaction/get_infos_by_order_ids'
		TRANSACTION_UPDATE_PAYMENT = '/transaction/update_payment'
		TRANSACTION_DELETE = '/transaction/delete'
		TRANSACTION_CREATE = '/transaction/create'

		URL_CREATE_SHORT_URL = '/url/create_short_url'
		URL_GET_SHORT_URL = '/url/get_short_url'

		USER_CHECK_SHIPPER_BONUS_EDITABLE = '/user/check_shipper_bonus_editable'
		USER_CHECK_VERIFIED = '/user/check_verified'
		USER_CLONE_FOODY_USER = '/user/clone_foody_user'
		USER_CREATE_EXTERNAL_TOKEN = '/user/create_external_token'
		USER_CREATE_FOODY_USER = '/user/create_foody_user'
		USER_CREATE_PROPERTY_MAPPING = '/user/create_customer_property_mapping'
		USER_CREATE_REQUEST_ORDER = '/user/create_request_order'
		USER_DELETE_INACTIVE_FOODY_USER = '/user/delete_inactive_foody_user'
		USER_DELETE_PROPERTY_MAPPING = '/user/delete_customer_property_mapping'
		USER_GET_ACCESSIBLE_PROJECTS = '/user/get_accessible_projects'
		USER_GET_ACCOUNTANT_INFO = '/user/get_accountant_info'
		USER_GET_CC_UIDS = '/user/get_cc_uids'
		USER_GET_CUSTOMER_PROPERTIES = '/user/get_customer_properties'
		USER_GET_CUSTOMER_PROPERTY_MAPPINGS = '/user/get_customer_property_mappings'
		USER_GET_EXTERNAL_TOKEN = '/user/get_external_token'
		USER_GET_FOODY_UID_BY_FOODY_TOKEN = '/user/get_foody_uid_by_foody_token'
		USER_GET_HR_EMPLOYEE_INFOS = '/user/get_hr_employee_infos'
		USER_GET_KEEP_AMOUNT_CONFIGS_BY_CITY_ID = '/user/get_shipper_keep_amount_configs_by_city_id'
		USER_GET_ROLES = '/user/get_roles'
		USER_GET_SHIPPER_INFOS = '/user/get_shipper_infos'
		USER_GET_SHIPPER_KEEP_AMOUNT = '/user/get_shipper_keep_amount'
		USER_GET_SHIPPER_KEEP_AMOUNT_CONFIG = '/user/get_shipper_keep_amount_config'
		USER_GET_SHIPPER_UIDS = '/user/get_shipper_uids'
		USER_GET_SOCIAL_AVATAR_INFO = '/user/get_social_avatar_info'
		USER_GET_UID_BY_PHONE = '/user/get_uid_by_phone'
		USER_GET_UID_BY_SOCIAL_MAPPING = '/user/get_uid_by_social_mapping'
		USER_GET_USER_AUTH_INFO = '/user/get_user_auth_info'
		USER_GET_USER_AUTH_INFO_BY_UID = '/user/get_user_auth_info_by_uid'
		USER_GET_USER_BASIC_INFOS = '/user/get_user_basic_infos'
		USER_GET_USER_EXTENDED_INFOS = '/user/get_user_extended_infos'
		USER_SEARCH_UIDS_BY_KEYWORD = '/user/search_uids_by_keyword'
		USER_SET_SOCIAL_MAPPING = '/user/set_social_mapping'
		USER_SET_USER_EXTENDED_INFO = '/user/set_user_extended_info'
		USER_UPDATE_AVATAR_INFO = '/user/update_avatar_info'
		USER_UPDATE_HR_EMPLOYEE = '/user/update_hr_employee'
		USER_UPDATE_PASSWORD = '/user/update_password'
		USER_UPDATE_SHIPPER = '/user/update_shipper'
		USER_UPDATE_SHIPPER_CONTACT = '/user/update_shipper_contact'
		USER_UPDATE_SHIPPER_KEEP_AMOUNT_CONFIG = '/user/update_shipper_keep_amount_config'
		USER_UPDATE_USER_BASIC_INFO = '/user/update_user_basic_info'

	def __init__(self, host, app_id, country='VN', language='vi', timeout=5, retry=3):
		self._host = host
		self._app_id = app_id
		self._country = country
		self._language = language
		self._timeout = timeout
		self._retry = retry

		self._request_id = random.randint(0, 10 ** 10)
		self._session = requests.Session()

	def _gen_header(self):
		return {
			'X-Foody-Request-Id': str(self._request_id),
			'X-Foody-Api-Version': FApiServiceClient.APP_VERSION,
			'X-Foody-App-Id': str(self._app_id),
			'X-Foody-Country': self._country,
			'X-Foody-Language': self._language
		}

	def _request(self, api, data, method):
		self._request_id += 1
		log.info("fapi_service_request|host=%s,api=%s,request_id=%s,method=%s,data=%s", self._host, api, self._request_id, method, data)
		headers = self._gen_header()
		timeout = self._timeout
		if api == self.Api.ORDER_UPDATE_STATUS:
			timeout = self.UPDATE_STATUS_TIMEOUT
		if method == "POST":
			response = self._session.post(self._host + api, data=to_json(data, ensure_bytes=True), headers=headers, timeout=timeout)
		else:
			response = self._session.get(self._host + api, params=data, headers=headers, timeout=timeout)
		if response.status_code != 200:
			log.error("fapi_service_request_fail|request_id=%s,status_code=%s,api=%s", self._request_id, response.status_code, api)
			raise FApiServiceBadStatus(self._request_id, response.status_code)

		result = response.json()
		result_code = result["result"]
		result_body = result.get("reply")
		return result_code, result_body

	def request(self, api, data, method="POST", disable_retry=False):
		if disable_retry:
			return self._request(api, data, method);
		else:
			retry_count = self._retry
			while True:
				retry_count -= 1
				try:
					result_code, result_body = self._request(api, data, method)
					if retry_count > 0 and result_code == FApiServiceClient.Result.ERROR_SERVER:
						log.warn("get_error_server|request_id=%s,retry_count=%s", self._request_id, retry_count)
					else:
						return result_code, result_body
				except requests.exceptions.ConnectTimeout:
					log.exception("fapi_service_request_timeout|request_id=%s", self._request_id)
					if retry_count == 0:
						raise FApiServiceTimeout(self._request_id)
				except FApiServiceBadStatus as error:
					log.exception("fapi_service_bad_status|request_id=%s,http_code=%s", self._request_id, error.http_status)
					if retry_count == 0:
						raise
				except Exception as error:
					log.exception("fapi_service_request_exception|request_id=%s", self._request_id)
					if retry_count == 0:
						raise
			return None, None
