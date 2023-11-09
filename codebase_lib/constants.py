from common.constants import *
from common.enum_type import EnumBase

class Result(BaseResult):
	ERROR_MISSING_AUTH_CONFIG = "error_missing_auth_config"
	ERROR_SERVER_MAINTENANCE = "error_server_maintenance"
	ERROR_FORBIDDEN = "error_forbidden"
	ERROR_NOT_FOUND = "error_not_found"
	ERROR_NOT_IN_WHITE_LIST = "error_not_in_white_list"
	ERROR_APP_TYPE_INVALID = "error_app_type_invalid"
	ERROR_SIGNATURE = "error_signature"
	ERROR_ACCESS_TOKEN = "error_access_token"
	ERROR_ACCOUNT_INVALID = "error_account_invalid"
	ERROR_ACCOUNT_INACTIVE = "error_account_inactive"
	# ERROR_INVALID_HR_EMPLOYEE = "error_invalid_hr_employee"
	ERROR_PRELOGIN_NOT_FOUND = "error_prelogin_not_found"
	ERROR_PRE_CHANGE_PASS_NOT_FOUND = "error_pre_change_pass_not_found"
	ERROR_PRE_CONFIRM_PASSWORD_NOT_FOUND = "error_pre_confirm_password_not_found"
	ERROR_FORCE_LOGOUT = "error_force_logout"
	ERROR_AUTH = "error_auth"
	ERROR_SHORT_PASS = "error_short_pass"
	ERROR_TOKEN_EXIST = "error_token_exist"
	ERROR_ACCOUNT_EXISTED = "error_account_existed"
	ERROR_PRE_REGISTER_NOT_FOUND = "error_pre_register_not_found"
	ERROR_PRE_REGISTER_NOT_MATCH = "error_pre_register_not_match"
	ERROR_INVALID_NAME = "error_invalid_name"
	ERROR_TOKEN_VALIDATION_FAILED = "error_token_validation_failed"
	ERROR_ACCOUNT_DELETED = "error_account_deleted"
	ERROR_ACCOUNT_BLOCKED = "error_account_blocked"
	ERROR_USERNAME_INVALID = "error_username_invalid"
	ERROR_USERNAME_EXISTED = "error_username_existed"
	ERROR_USERNAME_USED_IN_PASS = "error_username_used_in_pass"
	ERROR_USERNAME_INVALID_LENGTH = "error_username_invalid_length"
	ERROR_USERNAME_INVALID_CHARS = "error_username_invalid_chars"
	ERROR_INVALID_TOKEN = "error_invalid_token"
	# ERROR_INVALID_FOODY_TOKEN = "error_invalid_foody_token"
	ERROR_PRE_STEP_NOT_FOUND = "error_pre_step_not_found"
	ERROR_PRE_STEP_NOT_MATCH = "error_pre_step_not_match"
	ERROR_INVALID_CLIENT_VERSION = "error_invalid_client_version"
	ERROR_INVALID_URL = "error_invalid_url"
	ERROR_INVALID_DATE_FORMAT = "error_invalid_date_format"
	ERROR_HAS_NO_PERMISSION = "error_has_no_permission"
	ERROR_DATA_NOT_CHANGED = "error_data_not_changed"

	ERROR_INVALID_TRIP_PLAN = "error_invalid_trip_plan"
	ERROR_INVALID_TRIP_PLAN_DAY = "error_invalid_trip_plan_day"
	ERROR_CANNOT_CREATE_TRIP_PLAN = "error_cannot_create_trip_plan"
	ERROR_CANNOT_CREATE_TRIP_PLAN_DAY = "error_cannot_create_trip_plan_day"
	ERROR_CANNOT_CREATE_TRIP_PLAN_ACTIVITY = "error_cannot_create_trip_plan_activity"
	ERROR_CANNOT_UPDATE_TRIP_PLAN = "error_cannot_update_trip_plan"
	ERROR_CANNOT_UPDATE_TRIP_PLAN_LOCATION = "error_cannot_update_trip_plan_locations"
	ERROR_CANNOT_UPDATE_TRIP_PLAN_DAY = "error_cannot_update_trip_plan_day"
	ERROR_CANNOT_UPDATE_TRIP_PLAN_ACTIVITY = "error_cannot_update_trip_plan_activity"
	ERROR_CANNOT_DELETE_TRIP_PLAN = "error_cannot_delete_trip_plan"
	ERROR_CANNOT_DELETE_TRIP_PLAN_DAY = "error_cannot_delete_trip_plan_day"
	ERROR_CANNOT_DELETE_TRIP_PLAN_ACTIVITY = "error_cannot_delete_trip_plan_activity"
	ERROR_CANNOT_UPDATE_TRIP_PLAN_ACTIVITIES = "error_cannot_update_trip_plan_activities"
	ERROR_CANNOT_DELETE_ACTIVITIES_BY_DATE = "error_cannot_delete_activities_by_date"
	ERROR_CANNOT_CLONE_TRIP = "error_cannot_clone_trip"

	ERROR_INVALID_PLACE = "error_invalid_place"
	ERROR_FETCH_GOOGLE_PLACE_FAILED = "error_fetch_google_place_failed"
	ERROR_GOOGLE_SEARCH = "error_google_search"
	ERROR_GOOGLE_SEARCH_EXCEED_QUOTA = "error_google_search_exceed_quota"
	ERROR_GOOGLE_SEARCH_NOT_FOUND = "error_google_search_not_found"
	ERROR_LOCATION_NOT_FOUND = "error_location_not_found"
	ERROR_PLACE_NOT_FOUND = "error_place_not_found"

	ERROR_USER_UPDATE_PROFILE = "error_user_update_profile"
	ERROR_USER_SEND_FEEDBACK = "error_cannot_send_feedback"
	ERROR_USER_UPLOAD_AVATAR = "error_user_upload_avatar"
	ERROR_USER_CREATE_CUSTOM_PLACE = "error_user_create_custom_place"
	ERROR_USER_HAS_NO_POINT = "error_user_has_no_point"

	ERROR_USERNAME_REQUIRED = "error_username_required"
	ERROR_USERNAME_CANNOT_UPDATED = "error_username_cannot_updated"

	ERROR_USER_COLLECTION_NOT_EXIST = "error_collection_not_exists"
	ERROR_USER_COLLECTION_ITEM_NOT_EXIST = "error_collection_item_not_exist"
	ERROR_USER_REMOVE_SAVE_PLAN_COLLECTION = "error_remove_user_plan_collection"
	ERROR_SAVED_PLAN_COLLECTION_NOT_EXIST = "error_saved_plan_collection_not_exist"
	ERROR_SAVED_PLAN_COLLECTION_ITEM_NOT_EXIST = "error_saved_plan_collection_item_not_exist"
	ERROR_SAVED_PLAN_CANNOT_ADD_ITEM = "error_saved_plan_cannot_add_item"
	ERROR_SAVED_ARTICLE_CANNOT_ADD_ITEM = "error_saved_article_cannot_add_item"
	ERROR_SAVED_ARTICLE_COLLECTION_NOT_EXIST = "error_saved_article_collection_not_exist"
	ERROR_SAVED_ARTICLE_COLLECTION_ITEM_NOT_EXIST = "error_saved_article_collection_item_not_exist"
	ERROR_LIKED_PLAN_CANNOT_ADD_ITEM = "error_liked_plan_cannot_add_item"
	ERROR_LIKED_PLAN_COLLECTION_NOT_EXIST = "error_liked_plan_collection_not_exist"
	ERROR_LIKED_PLACE_COLLECTION_NOT_EXIST = "error_liked_place_collection_not_exist"
	ERROR_COMMENT_CANNOT_SAVED = "error_comment_cannot_saved"
	ERROR_COMMENT_INVALID_CONTENT = "error_comment_invalid_content"
	ERROR_COMMENT_CANNOT_REMOVED = "error_cannot_remove_comment"
	ERROR_CANNOT_DELETE_ARTICLES = "error_cannot_delete_articles"
	ERROR_SAVED_PLACE_COLLECTION_NOT_EXIST = "error_saved_place_collection_not_exist"

	ERROR_DEVICE_CANNOT_REGISTER_TOKEN = "error_device_cannot_register_token"
	ERROR_DEVICE_CANNOT_UPDATE_SETTINS = "error_device_cannot_update_settings"

	ERROR_USER_UPLOAD_AVATAR_INVALID_FILE = "error_user_upload_avatar_invalid_file"
	ERROR_USER_UPLOAD_COVER_INVALID_FILE = "error_user_upload_cover_invalid_file"
	ERROR_USER_UPLOAD_COVER = "error_user_upload_cover"

	ERROR_PLAN_UPLOAD_COVER_INVALID_FILE = "error_plan_upload_cover_invalid_file"
	ERROR_PLAN_UPLOAD_COVER = "error_plan_upload_cover"

	ERROR_CAMPAIGN_INVALID = "error_campaign_invalid"
	ERROR_CAMPAIGN_INVALID_MEMBER = "error_campaign_invalid_member"
	ERROR_CAMPAIGN_REGISTER_INVALID_INFO = "error_campaign_register_invalid_info"
	ERROR_CAMPAIGN_REGISTER_ALREADY_JOINED = "error_campaign_register_already_joined"
	ERROR_CAMPAIGN_INVALID_REFERRAL = "error_campaign_invalid_referral"
	ERROR_CAMPAIGN_ERROR_WHILE_SPIN = "error_campaign_while_spin"
	ERROR_CAMPAIGN_UNAVAILABLE_SPIN = "error_campaign_unavailable_spin"
	ERROR_CAMPAIGN_EXIST_SHARE_POST = "error_campaign_exist_share_post"
	ERROR_CAMPAIGN_SPIN_LOCK = "error_campaign_spin_lock"
	ERROR_CAMPAIGN_GET_LOCK = "error_campaign_get_lock"

	ERROR_ARTICLE_INVALID = "error_article_invalid"

	ERROR_BANNERS_INVALID = "error_banners_invalid"
	ERROR_CANNOT_CLEAR_CACHE = "error_cannot_clear_cache"

	ERROR_PHOTO_ALBUM_NAME_EXISTED = "error_album_name_existed"
	ERROR_PHOTO_ALBUM_CANNOT_UPDATED = "error_album_cannot_updated"
	ERROR_PHOTO_ALBUM_CANNOT_DELETED = "error_album_cannot_deleted"
	ERROR_PHOTO_UPLOAD_INVALID_FILE = "error_photo_upload_invalid_file"
	ERROR_PHOTO_UPLOAD_FAILED = "error_photo_upload_failed"
	ERROR_PHOTO_CANNOT_UPDATED = "error_photo_cannot_updated"
	ERROR_PHOTO_CANNOT_DELETE = "error_photo_cannot_deleted"

	ERROR_CANNOT_UPDATE_REVIEW = "error_cannot_update_review"
	ERROR_CANNOT_DELETE_REVIEW = "error_cannot_delete_review"
	ERROR_EXISTED_EMAIL = "error_existed_email"
	ERROR_INVALID_EMAIL = "error_invalid_email"
	ERROR_CANNOT_CREATE_USER = "error_cannot_create_user"
	ERROR_WRONG_OLD_PASSWORD = "error_wrong_old_password"
	ERROR_CANNOT_CHANGE_PASSWORD = "error_cannot_change_password"
	ERROR_CANNOT_RESET_PASSWORD = "error_cannot_reset_password"
	ERROR_CANNOT_UPDATE_STATUS = "error_cannot_update_status"
	ERROR_CANNOT_UPDATE = "error_cannot_update"
	ERROR_CANNOT_DELETE = "error_cannot_delete"
	ERROR_CANNOT_ADD = "error_cannot_add"
	ERROR_CANNOT_UPLOAD_FILE = "error_cannot_upload_file"

	ERROR_CANNOT_FOLLOW = "error_cannot_follow"
	ERROR_PLAN_PROCESSING_STATUS = "error_plan_processing_status"
	ERROR_APPROVE_POINT_CANNOT_SUBMIT = "error_approve_point_cannot_submit"
	ERROR_APPROVE_POINT_CANNOT_CANCEL = "error_approve_point_cannot_cancel"
	ERROR_APPROVE_POINT_CANNOT_UPDATE_STATUS = "error_approve_point_cannot_update_status"
	ERROR_APPROVE_POINT_INVALID_STATUS = "error_approve_point_invalid_status"
	ERROR_APPROVE_POINT_INVALID_TIME = "error_approve_point_invalid_time"
	ERROR_LIKED_PLACE_CANNOT_ADD_ITEM = "error_liked_place_cannot_add_item"
	ERROR_SAVED_PLACE_CANNOT_ADD_ITEM = "error_saved_place_cannot_add_item"
	ERROR_SUBMIT_EMPTY_PLAN = "error_submit_empty_plan"
	ERROR_MEMBER_EXISTED = "error_member_existed"
	ERROR_INVALID_CODE = "error_invalid_code"
	ERROR_EXPIRED = "error_expired"

	ERROR_APP_STATS_UPLOAD_INVALID_FILE = "error_app_stats_upload_invalid_file"
	ERROR_GOOGLE_CATEGORY_INVALID = "error_google_category_invalid"

	ERROR_CANNOT_CREATE_CHAT_USER = "error_cannot_create_chat_user"

	ERROR_CANNOT_GET_ALBUM = "error_cannot_get_album"
	ERROR_CANNOT_CREATE_ALBUM = "error_cannot_create_album"
	ERROR_ALBUM_NOT_EXISTED = "error_album_not_existed"

	ERROR_NAME_EXISTED = "error_name_existed"
	ERROR_PURPOSE_NOT_EXISTED = "error_purpose_not_existed"

class SolrEndpoint(EnumBase):
	url = 1


class RunningEnvironment(EnumBase):
	PRODUCTION = 1
	TESTING = 2
	DEVELOPMENT = 3
	STAGING = 4

class AppType(EnumBase):
	COOKY_APP = 1001
	COOKY_SERVER = 3001

class ServiceType(EnumBase):
	AUTH_API = 2000
	APP_API = 2001
	NOTIFY_API = 2002
	SEARCH_API = 2003
	MEDIA_API = 2004
	SERVICE_API = 2005
	CODEBASE_API = 2006
	PAYADMIN_API = 2007
	CRON_SERVICE = 9000
	QUEUED_SERVICE = 9001

class AppFlag(EnumBase):
	SINGLE_SESSION = 1

# alphabet
class AccountType(EnumBase):
	ACCOUNT_TYPE_EMAIL = 1
	ACCOUNT_TYPE_USERNAME = 2

class AccountStatus(EnumBase):
	DELETED = -1
	INACTIVE = 0
	ACTIVE = 1
	BLOCKED = 2

class AuthActionType(EnumBase):
	NONE = 0
	SET_PASSWORD = 1

class ClientType(EnumBase):
	SERVER = 0
	WEB = 1
	IOS = 2
	ANDROID = 3

class CountryCode:
	VIETNAM = "VN"

class GenderType(EnumBase):
	UNDEFINED = 0
	MALE = 1
	FEMALE = 2

class GenderTypeChar:
	MALE = ('m', 'male')
	FEMALE = ('f', 'female')

class LoginType(EnumBase):
	PASSWORD = 0
	FACEBOOK = 1
	GOOGLE = 2
	ACCOUNT_KIT = 3

class MailPriority(EnumBase):
	NORMAL = 5
	HIGH = 10

class Password(EnumBase):
	GENERATOR_SALT_SIZE = 5
	GENERATOR_PASS_SIZE = 5

class PasswordFormat(EnumBase):
	CLEAR = 0
	HASHED = 1
	ENCRYPTED = 2

class PhoneMappingType(EnumBase):
	ACCOUNT_KIT = 1
	MANUAL = 2

class ToggleType(EnumBase):
	OFF = 0
	ON = 1

class QueuedEmailStatus(EnumBase):
	PENDING = 1
	PROCESSING = 2
	SENT = 3
	FAILED = 4

class SendEmailResult(EnumBase):
	INVALID_EMAIL = 1
	INVALID_TEMPLATE = 2
	INVALID_EMAIL_ACCOUNT = 3
	SEND_EXCEPTION = 4


class UsePhoneStatus(EnumBase):
	VERIFIED = 1

class CommonStatus(EnumBase):
	DELETED = -1
	IN_ACTIVE = 0
	ACTIVE = 1

class TripPlanPublishType(EnumBase):
	PUBLIC = 1
	PRIVATE = 2

class TripPlanLocationType(EnumBase):
	DEPARTURE = 1
	DESTINATION = 2

class TripPlanStatus(EnumBase):
	UPCOMING = 1
	ONGOING = 2
	PAST = 3

class TripPlanApprovalStatus(EnumBase):
	PENDING = 1		# DRAFT
	APPROVED = 2
	DENIED = 3
	SUBMITTED = 4
	PROCESSING = 5
	IGNORED = 6

class TripPlanBrowseType(EnumBase):
	ALL = 0
	SHOW_HOME = 1
	FEATURED = 2

class TripPlanSortType(EnumBase):
	LATEST = 1
	MOST_VIEWED = 2

# [deprecated]
class TripPlanFeaturedStatus(EnumBase):
	NONE = 0
	FEATURED = 1
	POPULAR = 2

class PlaceStatus(EnumBase):
	DELETED = -1
	NOT_APPROVED = 1
	APPROVED = 2
	TEMP_CLOSED = 3
	CLOSED = 4
	EDITING = 5
	NEED_APPROVE = 6
	GOOGLE_FETCHING = 7

class UserFeedbackStatus(EnumBase):
	NEW = 1
	RESOLVED = 2
	IGNORED = 3

class AsyncTaskStatus(EnumBase):
	PENDING = 1
	PROCESSING = 2
	COMPLETED = 3
	FAILED = 4

class NotifyType(EnumBase):
	UNKNOWN = 0
	NEWS = 1
	PRIVATE = 2

class NotifyStatus(EnumBase):
	PENDING = 1
	PROCESSING = 2
	NOTIFIED = 3
	FAILED = 4

class AsyncTaskType(EnumBase):
	APP_PUSH_TO_ENDPOINT = 1
	FETCHING_GOOGLE_PLACE = 2
	FETCHING_FACEBOOK_AVATAR = 3
	FETCHING_PLACE_GEOCODE = 4
	PLAN_ACTIVITY_UPDATE_DISTANCE = 5
	REGISTER_PUSH_DEVICE_TOKEN = 6
	FETCHING_GOOGLE_PHOTO = 7
	FETCHING_STATIC_MAP_IMAGE = 8
	SCRAPE_SEO_DATA = 9
	REWARD_NEW_USER = 10
	UPDATE_PLACE_STATS = 11
	FETCHING_GOOGLE_PLACE_NEARBY_DESTINATION = 12

class CollectionType(EnumBase):
	SAVED = 1
	LIKED = 2
	CUSTOM = 10

class GooglePlaceSyncStatus(EnumBase):
	JUST_MAPPED = 1
	FETCHED_DATA = 2

class ArticleSortType(EnumBase):
	LATEST = 1
	MOST_VIEW = 2

class ArticleType(EnumBase):
	NONE = 0
	FEATURED = 1
	SHOW_HOME = 2
	USER_GUIDE = 4

class ArticleItemDataType(EnumBase):
	BROWSE = 1
	DETAILS = 2

class PlanInfoType(EnumBase):
	BROWSE = 1
	PRIVATE = 2
	PUBLIC = 3

class PlaceType(EnumBase):
	DESTINATION = 1
	NORMAL = 2

class ObjectType(EnumBase):
	PLAN = 1
	ARTICLE = 2
	USER = 3
	ARTICLE_LIST = 4
	PLAN_DISCOVER = 5
	PLACE = 6
	LINK = 7
	PHOTO = 8
	PHOTO_ALBUM = 9
	REVIEW = 10
	ACTIVITY = 11
	DESTINATION = 12
	PLAN_INVITE_LINK = 13
	CATEGORY = 14
	KEYWORD = 15
	CATEGORY_GROUP = 16
	ALBUM = 17

class ScreenType(EnumBase):
	PLAN = 1
	ARTICLE = 2
	USER = 3
	ARTICLE_LIST = 4
	PLAN_DISCOVER = 5
	PLACE = 6
	LINK = 7
	PHOTO = 8
	PHOTO_ALBUM = 9
	REVIEW = 10
	ACTIVITY = 11
	DESTINATION = 12
	USER_POINT_HISTORY = 13
	LUCKY_DRAW = 14
	PLAN_INVITE = 15

class CampaignMemberReferralType(EnumBase):
	SHARED_POST = 1
	INVITATION = 2

class CampaignChanceSourceType(EnumBase):
	DAILY = 1
	REFERRAL = 2

class CampaignRewardStatus(EnumBase):
	PENDING = 1
	DELIVERED = 2

class CampaignChanceHistoryValue(EnumBase):
	POINT_VALUE = 1
	REWARD_ITEM_CODE = 2

class CampaignResultType(EnumBase):
	REWARD = 1
	POINT = 2

class UserPointTxnStatus(EnumBase):
	PENDING = 1
	APPROVED = 2
	DENIED = 3

class UserPointTxnType(EnumBase):
	REWARD = 1
	USED = 2

class UserPointTxnRefType(EnumBase):
	REVIEW = 1
	PLAN = 2
	LUCKY = 3
	REDEEM = 4
	REGISTER = 5

class CampaignBlackListType(EnumBase):
	MEMBER_ID = 1
	IP = 2

class SearchIndexPushType(EnumBase):
	PLACE = 1
	PLAN = 2
	PLAN_DESTINATION = 3

class TripPlanPurpose(EnumBase):
	HOLIDAY = 1
	BUSINESS = 2

class GooglePlaceSortType(EnumBase):
	PROMINENCE = 1
	DISTANCE = 2

class TripPlanPriceLevel(EnumBase):
	CHEAP = 1
	# AVERAGE = 2
	LUXURY = 3

class AuthInfoHistoryType(EnumBase):
	USERNAME = 1
	EMAIL = 2
	PASSWORD = 3

class NewsPushStatus(EnumBase):
	PENDING = 1
	PROCESSING = 2
	COMPLETED = 3
	ERROR = 4

class ActionType(EnumBase):
	LIKE = 1
	COMMENT = 2
	FOLLOW = 3
	REGISTER_ACCOUNT = 4
	REWARD_POINT = 5
	INVITE_TO_TRIP = 6
	JOIN_TRIP = 7
	NEW_PLACE_TO_TRIP = 8

class EmailSubscriptionStatus(EnumBase):
	IN_ACTIVE = 0
	ACTIVE = 1
	SUBSCRIBED = 2

class ArticleStatus(EnumBase):
	DELETED = -1
	IN_ACTIVE = 0
	ACTIVE = 1
	WAITING = 2
	DRAFT = 3

class UserRoles:
	SUPER_ADMIN = "SUPER_ADMIN"
	ADMIN = "ADMIN"
	EDITOR = "EDITOR"
	COLLABORATORS = "TRIP_COLLABORATORS"
	APP_EDITOR = "APP_EDITOR"

class AlbumType(EnumBase):
	DEFAULT = 1		# default album, system created for user
	CUSTOM = 2		# album created by user

class PhotoGroupBy(EnumBase):
	ALBUM = 1
	PLACE = 2
	PLAN = 3

class FollowType(EnumBase):
	FOLLOWER = 1
	FOLLOWING = 2

class GoogleMappingPlaceType(EnumBase):
	COUNTRY = 1
	CITY = 2
	DISTRICT = 3
	PLACE = 4
	PROVINCE = 5
	NEW_CITY = 6
	NEW_PROVINCE = 7

class ResourceKey:
	place_status_closed = "place_status_closed"
	place_status_temp_closed = "place_status_temp_closed"
	place_status_unverified = "place_status_unverified"
	place_status_verify = "place_status_verify"
	trip_to = "trip_to"
	plan_transaction_name = "PLAN_TRANSACTION_NAME"
	lucky_transaction_name = "LUCKY_TRANSACTION_NAME"
	redeem_transaction_name = "REDEEM_TRANSACTION_NAME"
	review_transaction_name = "REVIEW_TRANSACTION_NAME"
	user_transaction_name = "USER_TRANSACTION_NAME"
	trip_auto_name = "trip_auto_name"
	trip_auto_name_with_price = "trip_auto_name_with_price"
	trip_generate_name = "trip_generate_name"
	review_generate_title = "review_generate_title"

class ReviewRating(EnumBase):
	OK = 1
	HAPPY = 2
	UNHAPPY = 3

class DefaultImageKey(EnumBase):
	PLACE = "place"
	CATEGORY_GROUP_FOOD = "category_group_food"
	CATEGORY_GROUP_ENTERTAINMENT = "category_group_entertainment"
	CATEGORY_GROUP_BEAUTY = "category_group_beauty"
	CATEGORY_GROUP_TRAVEL = "category_group_travel"
	CATEGORY_GROUP_SHOPPING = "category_group_shopping"
	CATEGORY_GROUP_EDUCATION = "category_group_education"
	CATEGORY_GROUP_WEDDING = "category_group_wedding"
	CATEGORY_GROUP_SERVICE = "category_group_service"
	CATEGORY_GROUP_LODGING = "category_group_lodging"
	CATEGORY_GROUP_TRANSPORT = "category_group_transport"
	CATEGORY_GROUP_TOUR = "category_group_tour"
	CATEGORY_GROUP_SPECIAL = "category_group_special"

class FaktoryJobType:
	SEND_EMAIL = "send_email"
	PUSH_NOTIFICATION = "push_notification"
	SYNC_MEDIA = "sync_media"

class PointPropertyType(EnumBase):
	PHOTO = 1
	PLAN_NOTE_LENGTH = 2
	PLAN_QUALITY = 3
	PLAN_DURATION = 4
	PLAN_SCOPE = 5
	PLAN_COST = 6
	REVIEW_LENGTH = 7
	NEW_USER = 8

class PlanScope(EnumBase):
	DOMESTIC = 1
	INTERNATIONAL = 2

class PlanQuality(EnumBase):
	UNKNOWN = 0
	ACCEPTABLE = 1
	PROFESSIONAL = 2

class DiscountType(EnumBase):
	VALUE = 1
	PERCENT = 2

class SearchSortType(EnumBase):
	BEST_MATCH = 1
	NEARBY = 2
	POPULAR = 3
	LATEST = 4
	TOP = 5

class MergePlaceType(EnumBase):
	MERGE = 1
	ADOPT = 2
class InviteStatus(EnumBase):
	DELETED = -1
	ACTIVE = 1
	WAITING = 2
	REJECT = 3
	LEAVE = 4


class PlanMemberRole(EnumBase):
	OWNER = 1
	VIEWER = 2
	CONTRIBUTOR = 3
	PLANNER = 4

class PlanMemberAction(EnumBase):
	ALLOW_VIEW = 1
	ADD_ACTIVITY = 2
	DRAG_ACTIVITY = 3
	UPLOAD_PHOTO = 4
	INVITE_MEMBER = 5

class PlanMemberInviteFrom(EnumBase):
	UNKNOWN = 0
	ADDED = 1
	JOINED = 2

class GoogleKeyPaidType(EnumBase):
	FREE = 1
	PAID = 2

class SearchType(EnumBase):
	GOOGLE_AUTO_COMPLETE = 1
	GOOGLE_TEXT_SEARCH = 2
	GOOGLE_NEAR_BY_SEARCH = 3
	METRIP_PLACE_SEARCH = 4
	METRIP_DESTINATION_SEARCH = 5

class ExternalPostSort(EnumBase):
	OLDEST = 1
	LATEST = 2

class SendBirdTokenType(EnumBase):
	APNS = "apns"
	GCM = "gcm"

class ExternalArticleType(EnumBase):
	BLOG = 1
	VIDEO = 2

class SyncMediaType(EnumBase):
	CREATING = 1
	DELETING = 2

class MediaMetaStatus(EnumBase):
	SELF_HOSTED = 1
	SYNC_QUEUED = 2
	CLOUD_HOSTED = 3
	FILE_NOT_FOUND = 4
	FILE_NOT_READ = 5
	SYNC_CLOUD_FAILED = 6

