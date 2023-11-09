from common.datacache import DataCache
from .cache_manager import key_cache_data, simple_cache_data, CACHE_KEY_FUNC_SETTING_GENERAL, CACHE_KEY_FUNC_SETTING_ZONE, CACHE_KEY_FUNC_SETTING_FOODY_GENERAL
from .api_service_client import *
from .models import *
import ast
from codebase_lib.constants import DATETIME_FORMAT

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR

SETTING_CACHE_TIMEOUT = 5 * 60
SETTING_EMPTY_VALUE = -1
DELIVERY_SETTING_NONE_CITY_ID = 0

class SettingCache(DataCache):
	def _load_data(self):
		settings = MeTripDB.Setting.objects.all()
		result = {}
		for setting in settings:
			result[setting.name.lower()] = setting.value
		return result

	def get_setting(self, setting_name):
		return self.get_data().get(setting_name.lower(), None)

_setting_cache = SettingCache(SETTING_CACHE_TIMEOUT)

class SettingKey:
	ACCOUNT_KIT_ENDPOINT = 'user.auth.account_kit_endpoint'
	PUSH_NEW_TOPIC_NAME = "push.news.topic"
	HASH_IDS_MIN_LENGTH = "hashids.min.length"
	ALLOW_INTERNAL_DOMAIN = "allow.internal.domain"
	MAINTENANCE_SETTING = 'maintenance.settings'

class SettingKeyDefault:
	ACCOUNT_KIT_ENDPOINT = 'https://graph.accountkit.com'
	PUSH_NEW_TOPIC_NAME = "news-topic"
	HASH_IDS_MIN_LENGTH = 10
	ALLOW_INTERNAL_DOMAIN = "metrip.vn;billbros.vn"

def get_setting(name, default=None, use_cache=True):
	if not name:
		return default
	if use_cache:
		result = _setting_cache.get_setting(name)
	else:
		result = MeTripDB.Setting.objects.filter(name=name.lower()).values('value').first()
		if result:
			result = result['value']
	return result if result else default

def get_setting_boolean(name, default=None):
	setting_value = get_setting(name)
	if setting_value is None:
		setting_value = default
	elif isinstance(setting_value, str):
		setting_value = setting_value.lower() == "true"
	return setting_value

def get_setting_number(name, default=None, converter=int):
	setting_value = get_setting(name)
	if setting_value is None:
		setting_value = default
	return converter(setting_value)

def get_setting_list(name, default=None, converter=ast.literal_eval):
	setting_value = get_setting(name)
	if setting_value is None:
		setting_value = default
		return setting_value
	return converter(setting_value)

def get_setting_datetime(name, default=None, use_cache=True, dt_format=DATETIME_FORMAT):
	setting_value = get_setting(name, default, use_cache)
	# if setting_value is None:
	# 	setting_value = default
	if not setting_value:
		return None
	from codebase_lib.utils import parse_string_to_date
	return parse_string_to_date(setting_value, dt_format)

def set_setting(name, value):
	MeTripDB.Setting.objects.update_or_create(name=name,defaults={
		'value': value,
		'updated_on': datetime.now()
	})

# copy cat cache, will remove soon
def get_general_setting(name, default=None):
	results = get_general_settings([name])
	setting_value = results.get(name)
	if not setting_value or setting_value.strip() == '':
		setting_value = default
	return setting_value

def set_general_setting(name, value):
	request_data = {
		"name": name,
		"value": value
	}
	_, settings = request(FApiServiceClient.Api.SETTING_SET_GENERAL_SETTING, request_data)

def get_or_set_general_setting(name, default):
	setting_value = get_general_settings([name]).get(name)
	if not setting_value or setting_value.strip() == '':
		setting_value = default
		set_general_setting(name, default)
	return setting_value

def get_general_setting_number(name, default=None, converter=int):
	setting_value = get_general_setting(name, default)
	if setting_value is None:
		setting_value = 0
	else:
		setting_value = converter(setting_value)
	return setting_value

def get_general_setting_boolean(name, default):
	setting_value = get_general_setting(name, default)
	if setting_value is None:
		setting_value = False
	else:
		setting_value = setting_value.lower() == "true"
	return setting_value

@key_cache_data(**CACHE_KEY_FUNC_SETTING_GENERAL)
def get_general_settings(names):
	results = {}
	for name in names:
		results[name] = None
	_, settings = request(FApiServiceClient.Api.SETTING_GET_GENERAL_SETTINGS, {'names': names})
	if settings and 'settings' in settings:
		for setting_name in settings['settings']:
			results[setting_name] = settings['settings'][setting_name]
	return results

@key_cache_data(**CACHE_KEY_FUNC_SETTING_FOODY_GENERAL)
def get_foody_general_settings(names):
	results = {}
	for name in names:
		results[name] = None
	_, settings = request(FApiServiceClient.Api.SETTING_GET_FOODY_GENERAL_SETTINGS, {'names': names})
	if settings and 'settings' in settings:
		for setting_name in settings['settings']:
			results[setting_name] = settings['settings'][setting_name]
	return results

@simple_cache_data(lambda cache_prefix, name, city_id: cache_prefix % (name, city_id), **CACHE_KEY_FUNC_SETTING_ZONE)
def _get_zone_setting(name, city_id):
	data = {"name": name}
	result = None
	if city_id != DELIVERY_SETTING_NONE_CITY_ID:
		data['city_id'] = city_id
	_, settings = request(FApiServiceClient.Api.SETTING_GET_ZONE_SETTING, data)
	if settings and 'value' in settings:
		result = settings['value']
	return result

def get_zone_setting(name, city_id=DELIVERY_SETTING_NONE_CITY_ID, default=None):
	setting_value = _get_zone_setting(name, city_id)
	if setting_value is None and default is not None:
		setting_value = default
	return setting_value

def get_zone_setting_number(name, city_id=DELIVERY_SETTING_NONE_CITY_ID, default=None, converter=int):
	setting_value = get_zone_setting(name, city_id, default)
	if setting_value is None:
		setting_value = 0
	else:
		setting_value = converter(setting_value)
	return setting_value
