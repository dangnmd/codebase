from common.logger import log
from common.datacache import DataCache
from codebase_lib import config
from codebase_lib.constants import *
from .api_service_client import *
from .models import *
from codebase_lib.managers import setting_manager
import json
import re

DEFAULT_CACHE_TIMEOUT = 10 * 60

class AppIPCache(DataCache):
	def _load_data(self):
		app_ip_api_list = MeTripDB.AppApi.objects.all()
		result = {}
		for app_ip_api in app_ip_api_list:
			ip_api_dict = result.get(app_ip_api.service_id)
			if not ip_api_dict:
				ip_api_dict = {}
				result[app_ip_api.service_id] = ip_api_dict
			api_set = ip_api_dict.get(app_ip_api.ip)
			if not api_set:
				api_set = set()
				ip_api_dict[app_ip_api.ip] = api_set
			api_set.add(app_ip_api.api)
		return result

	def has_permission(self, service_id, ip, api):
		result = self.get_data()
		if not result.get(service_id):
			return False
		if not result[service_id].get(ip):
			return False
		return api in result[service_id][ip] or "*" in result[service_id][ip]

class AppCache(DataCache):
	def _load_data(self):
		app_info_list = MeTripDB.App.objects.all()
		result = {}
		for app_info in app_info_list:
			result[app_info.app_id] = app_info
		return result

	def get_app(self, app_id):
		return self.get_data().get(app_id)

class AppServiceMappingCache(DataCache):
	def _load_data(self):
		app_service_list = MeTripDB.AppServiceMapping.objects.filter(status=ToggleType.ON).all()
		result = {}
		for mapping in app_service_list:
			if (mapping.app_id, mapping.service_id, mapping.client_type) not in result:
				result[(mapping.app_id, mapping.service_id, mapping.client_type)] = {}
			result[(mapping.app_id, mapping.service_id, mapping.client_type)][mapping.min_client_version] = mapping
		return result

	def get_service_mapping(self, app_id, service_id, client_type, app_version):
		mappings = self.get_data().get((app_id, service_id, client_type))
		if not mappings:
			return None, None
		support_version = 100
		min_support_version = 100000
		for min_client_version, service_mapping in list(mappings.items()):
			if app_version >= min_client_version > support_version:
				support_version = min_client_version
			if min_support_version > min_client_version:
				min_support_version = min_client_version
		return min_support_version, mappings.get(support_version)

class AppMaintenanceCache(DataCache):
	def _load_data(self):
		maintenance_settings = MeTripDB.Setting.objects.filter(name=setting_manager.SettingKey.MAINTENANCE_SETTING).values('value').first()
		if not maintenance_settings or 'value' not in maintenance_settings:
			return {}
		json_data = json.loads(maintenance_settings['value'])
		if not json_data:
			return {}
		maintenance_dict = {}
		for setting in json_data:
			data_key = (setting['service_id'], setting['app_id'])
			maintenance_dict[data_key] = setting['url_patterns']
		return maintenance_dict

	def get_maintenance_status(self, service_id, app_id, request_url):
		url_patterns = self.get_data().get((service_id, app_id))
		if not url_patterns:
			return False
		is_maintenance = False
		for url_pattern in url_patterns:
			match_obj = re.match(url_pattern, request_url)
			if match_obj:
				is_maintenance = True
				log.info('service_maintenance|url=%s,service_id=%s,app_id=%s,matched_pattern=%s', request_url, service_id, app_id, match_obj.re.pattern)
				break
		return is_maintenance


_app_ip_cache = AppIPCache(DEFAULT_CACHE_TIMEOUT)
_app_cache = AppCache(DEFAULT_CACHE_TIMEOUT)
_app_service_cache = AppServiceMappingCache(DEFAULT_CACHE_TIMEOUT)
_app_maintenance_cache = AppMaintenanceCache(DEFAULT_CACHE_TIMEOUT)

def is_ip_white_listed(service_id, ip, api):
	return _app_ip_cache.has_permission(service_id, ip, api)

def get_app(app_id):
	return _app_cache.get_app(app_id)

def get_app_service_mapping(app_id, service_id, client_type, client_version):
	return _app_service_cache.get_service_mapping(app_id, service_id, client_type, client_version)

def is_url_maintenance(service_id, app_id, request_url):
	return _app_maintenance_cache.get_maintenance_status(service_id, app_id, request_url)
