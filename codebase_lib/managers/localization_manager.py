from .models import *
from codebase_lib.managers.cache_manager import simple_cache_data, CACHE_KEY_FUNC_GET_RESOURCE_VALUE
from common.i18n import _, add_i18n, I18N
from codebase_lib import traduora_service
from codebase_lib.managers import cache_manager
from common.logger import log
from common.utils import get_timestamp_ms
import requests
import json


class ResourceStringKey(object):
	NOTIFY_REGISTER_ACCOUNT = "notify_register_account"

def get_tradoura_access_token():
	return

def init_locales():
	if not config.LOCALE_CONFIG:
		return
	languages = config.LOCALE_CONFIG
	for language, data in list(languages.items()):
		url = data['url']
		locale = data['locale']
		i18n = request_locale(url)
		if not i18n:
			log.info('init_locales|load_from_local_file,locale=%s,url=%s', locale, url)
			import os
			import json
			local_file = os.path.dirname(os.path.abspath(__file__)) + '/../i18n/%s.json' % locale
			with open(local_file) as json_file:
				i18n = json.load(json_file)
		if not i18n:
			log.warn('init_locales|empty_locale_data,url=%s', url)
			continue
		add_i18n(language, i18n)


def request_locale(url):
	#dnguyen temporary return None because of no locale_url
	return None
	response = None
	start = get_timestamp_ms()
	try:
		response = requests.get(url, timeout=10)
		elapsed = int(get_timestamp_ms() - start)
		if response.status_code != 200:
			log.warn("request_locale_url|elapsed=%s,failed,url=%s,status_code=%s,response=%s", elapsed, url, response.status_code, response.text)
		else:
			log.info("request_locale_url|elapsed=%s,success,url=%s", elapsed, url)
			reply_data = {}
			if response.text != '':
				reply_data = json.loads(response.text)
			return reply_data
	except Exception as error:
		elapsed = int(get_timestamp_ms() - start)
		status_code = None
		if response and response.status_code:
			status_code = response.status_code
		log.exception("request_locale_url|exception=%s,elapsed=%s,failed,url=%s,request_data=%s,status_code=%s,response=%s", error, elapsed, url, request_data, status_code, '')
	return None

def get_locale(key, language=config.LANGUAGE):
	if not I18N:
		init_locales()
	return _(key, language)
