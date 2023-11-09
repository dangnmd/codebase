import time
from datetime import timedelta, datetime
from common import cache, jsonutils
from common.utils import get_timestamp, get_timestamp_ms, to_bytes, to_str
from common.logger import log
from codebase_lib import config
import re
from codebase_lib.constants import *

DEFAULT_EXPIRE = 60 * 60
DEFAULT_SHORT_EXPIRE = 5 * 60

CACHE_KEY_FUNC_GET_USER_INFO = {
	'cache_prefix': 'usr.%s',
	'expiry_time': 10 * 60,
	'cache_name': 'default'
}

CACHE_KEY_FUNC_GET_UID_BY_GROUP = {
	'cache_prefix': 'get_uid_by_group.%s',
	'expiry_time': DEFAULT_SHORT_EXPIRE,
	'cache_name': 'default'
}

CACHE_KEY_FUNC_SETTING_GENERAL = {
	'cache_prefix': 'g.setting.%s',
	'expiry_time': DEFAULT_SHORT_EXPIRE,
	'cache_name': 'default'
}

CACHE_KEY_FUNC_SETTING_FOODY_GENERAL = {
	'cache_prefix': 'f.setting.%s',
	'expiry_time': DEFAULT_SHORT_EXPIRE,
	'cache_name': 'default'
}

CACHE_KEY_FUNC_SETTING_ZONE = {
	'cache_prefix': 'z.setting.%s.%s',
	'expiry_time': DEFAULT_SHORT_EXPIRE,
	'cache_name': 'default'
}

CACHE_KEY_FUNC_GET_RESOURCE_VALUE = {
	'cache_prefix': 'get_resource_value.%s.%s.%s.%s',
	'expiry_time': DEFAULT_SHORT_EXPIRE,
	'cache_name': 'default'
}

CACHE_KEY_GET_PUSH_TOPIC_BY_CODE = {
	'cache_prefix': 'get_push_topic.%s',
	'expiry_time': DEFAULT_SHORT_EXPIRE,
	'cache_name': 'default'
}

CACHE_KEY_VNG_CLOUD_AUTHENTICATION = {
	'cache_prefix': 'vng_cloud_authentication',
	'expiry_time': DEFAULT_EXPIRE - 60,
	'cache_name': 'default'
}

if hasattr(config, 'CACHE_SERVERS'):
	cache.init_cache(config.CACHE_SERVERS)

# some simple decorators to cache data
def simple_cache_data(cache_key_converter, cache_prefix, expiry_time=60, cache_name="default"):
	def _cache_data(func):
		def _func(*args, **kwargs):
			cache_key = cache_key_converter(cache_prefix, *args)
			start_time = get_timestamp_ms()
			data = cache.get_cache(cache_name).get(cache_key)
			force_query = kwargs.get("force_query", False)
			if force_query or data is None:
				data = func(*args)
				if data is None:
					log.info("cache_set|data=None,cache_key=%s,force_query=%s", cache_key, force_query)
					return None
				cache.get_cache(cache_name).set(cache_key, data, expiry_time)
				end_time = get_timestamp_ms()
				log.info("cache_set|elapsed=%s,cache_key=%s,force_query=%s", end_time - start_time, cache_key, force_query)
			else:
				end_time = get_timestamp_ms()
				log.info("cache_hit|elapsed=%s,cache_key=%s", end_time - start_time, cache_key)
			update_cache_func = kwargs.get('update_cache_func', None)
			if update_cache_func:
				data = update_cache_func(data)
				cache.get_cache(cache_name).set(cache_key, data, expiry_time)
				log.info("cache_update_data|cache_key=%s", cache_key)
			return data

		return _func

	return _cache_data

def simple_cache_data_with_log_key(cache_key_converter, cache_prefix, expiry_time=60, cache_name="default"):
	def _cache_data(func):
		def _func(*args, **kwargs):
			log_key, cache_key = cache_key_converter(cache_prefix, *args)
			start_time = get_timestamp_ms()
			data = cache.get_cache(cache_name).get(cache_key)
			force_query = kwargs.get("force_query", False)
			if force_query or data is None:
				data = func(*args)
				cache.get_cache(cache_name).set(cache_key, data, expiry_time)
				end_time = get_timestamp_ms()
				log.info("cache_set|elapsed=%s,log_key=%s,cache_key=%s,force_query=%s", end_time - start_time, log_key, cache_key, force_query)
			else:
				end_time = get_timestamp_ms()
				log.info("cache_hit|elapsed=%s,log_key=%s,cache_key=%s", end_time - start_time, log_key, cache_key)
			update_cache_func = kwargs.get('update_cache_func', None)
			if update_cache_func:
				data = update_cache_func(data)
				cache.get_cache(cache_name).set(cache_key, data, expiry_time)
				log.info("cache_update_data|cache_key=%s", cache_key)
			return data

		return _func

	return _cache_data

# input: must be a list
# output: must be a dict
def key_cache_data(cache_prefix, expiry_time=60, cache_name="default"):
	def _cache_data(func):
		def _func(keys, **kwargs):
			if not keys:
				return {}
			keys = list(set(keys))
			force_query = kwargs.get("force_query", False)
			result_data = {}
			if not force_query:
				start_time = get_timestamp_ms()
				cache_key_map = {cache_prefix % key: key for key in keys}
				cached_data_dict = cache.get_cache(cache_name).get_many(list(cache_key_map.keys()))
				for cached_key, cached_data in list(cached_data_dict.items()):
					key = cache_key_map[cached_key]
					result_data[key] = cached_data
					keys.remove(key)
				end_time = get_timestamp_ms()
				log.info("key_cache_hit|elapsed=%s,cache_keys=%s", end_time - start_time, ','.join(list(cached_data_dict.keys())))
			if keys:
				response_data = func(keys)
				if response_data:
					start_time = get_timestamp_ms()
					data_to_cache = {cache_prefix % key: data for key, data in list(response_data.items())}
					cache.get_cache(cache_name).set_many(data_to_cache, expiry_time)
					end_time = get_timestamp_ms()
					log.info("key_cache_set|elapsed=%s,cache_keys=%s", end_time - start_time, ','.join(list(data_to_cache.keys())))
				return dict(list(result_data.items()) + list(response_data.items()))
			else:
				return result_data

		return _func

	return _cache_data

def clear_cache(*args, **cache_key):
	cache_name = cache_key.get('cache_name', 'default')
	cache_prefix = cache_key.get('cache_prefix', '')
	if args:
		cache_prefix = cache_prefix % args
	return cache.get_cache(cache_name).delete(cache_prefix)

def clear_cache_by_key(cache_key, cache_name='default'):
	return cache.get_cache(cache_name).delete(cache_key)

def clear_cache_by_pattern(pattern, cache_name='default'):
	if "%s" in pattern:
		pattern = pattern.replace("%s", "*")
	return cache.get_cache(cache_name).delete_by_pattern(pattern)
