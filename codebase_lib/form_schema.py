from common.form_validator import extend_form_schema
from codebase_lib.constants import *

def enum_limit(enum_cls):
	return {'min_value': enum_cls.MIN_VALUE, 'max_value': enum_cls.MAX_VALUE}

UInt8Schema = {"type": "integer", "minimum": 0, "maximum": TYPE_UINT8_MAX}
UInt16Schema = {"type": "integer", "minimum": 0, "maximum": TYPE_UINT16_MAX}
UInt32Schema = {"type": "integer", "minimum": 0, "maximum": TYPE_UINT32_MAX}
Int32Schema = {"type": "integer", "minimum": TYPE_INT32_MIN, "maximum": TYPE_INT32_MAX}
UInt64Schema = {"type": "integer", "minimum": 0, "maximum": TYPE_UINT64_MAX}
UFloatSchema = {"type": "number", "minimum": 0}
DoubleSchema = {"type": "number"}
StringSchema = {"type": "string"}
BooleanSchema = {"type": "boolean"}
PasswordHashSchema = {"type": "string"}
IdSchema = {"type": "integer", "minimum": 1, "maximum": TYPE_UINT64_MAX}
AccountTypeSchema = {"type": "integer", "minimum": AccountType.MIN_VALUE, "maximum": AccountType.MAX_VALUE}
ClientTypeSchema = {"type": "integer", "minimum": ClientType.MIN_VALUE, "maximum": ClientType.MAX_VALUE}
AppTypeSchema = {"type": "integer", "minimum": AppType.MIN_VALUE, "maximum": AppType.MAX_VALUE}
GenderTypeSchema = {"type": "integer", "minimum": GenderType.MIN_VALUE, "maximum": GenderType.MAX_VALUE}
LoginTypeSchema = {"type": "integer", "minimum": LoginType.MIN_VALUE, "maximum": LoginType.MAX_VALUE}
TripPlanPublishTypeSchema = {"type": "integer", "minimum": TripPlanPublishType.MIN_VALUE, "maximum": TripPlanPublishType.MAX_VALUE}
TripPlanLocationTypeSchema = {"type": "integer", "minimum": TripPlanLocationType.MIN_VALUE, "maximum": TripPlanLocationType.MAX_VALUE}
TripPlanStatusSchema = {"type": "integer", "minimum": TripPlanStatus.MIN_VALUE, "maximum": TripPlanStatus.MAX_VALUE}
PlanBrowseTypeSchema = {"type": "integer", "minimum": TripPlanBrowseType.MIN_VALUE, "maximum": TYPE_UINT8_MAX}
PlanSortTypeSchema = {"type": "integer", "minimum": TripPlanSortType.MIN_VALUE, "maximum": TripPlanSortType.MAX_VALUE}
ArticleSortTypeSchema = {"type": "integer", "minimum": ArticleSortType.MIN_VALUE, "maximum": ArticleSortType.MAX_VALUE}
ArticleTypeSchema = {"type": "integer", "minimum": ArticleType.MIN_VALUE, "maximum": ArticleType.MAX_VALUE}
PlaceTypeSchema = {"type": "integer", "minimum": PlaceType.MIN_VALUE, "maximum": PlaceType.MAX_VALUE}
EmptyTypeSchema = {"type": "object", "properties": {}}
ArticleStatusSchema = {"type": "integer", "minimum": ArticleStatus.MIN_VALUE, "maximum": ArticleStatus.MAX_VALUE}
LatLngSchema = {
	"type": "object",
	"properties": {
		"lat": {
			"type": "number",
			"minimum": -90,
			"maximum": 90
		},
		"lng": {
			"type": "number",
			"minimum": -180,
			"maximum": 180
		},
		"required": ["lat", "lng"]
	}
}
ImageSizeSchema = {"type": "object", "properties": {"width": Int32Schema, "height": Int32Schema}, "required": ["width"]}
AccountStatusSchema = {"type": "integer", "minimum": AccountStatus.MIN_VALUE, "maximum": AccountStatus.MAX_VALUE}
PagingSchema = {
	"type": "object",
	"properties": {
		"page_index": {
			"type": "integer",
			"minimum": 1,
			"maximum": TYPE_INT32_MAX
		},
		"page_size": {
			"type": "integer",
			"minimum": 1,
			"maximum": TYPE_INT32_MAX
		}
	},
	"required": []
}
UserFeedbackStatusSchema = {"type": "integer", "minimum": UserFeedbackStatus.MIN_VALUE, "maximum": UserFeedbackStatus.MAX_VALUE}
PlaceStatusSchema = {"type": "integer", "minimum": PlaceStatus.MIN_VALUE, "maximum": PlaceStatus.MAX_VALUE}
