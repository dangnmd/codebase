import requests
from common.logger import log
from codebase_lib import config
from codebase_lib.utils import get_timestamp_ms
import time

prerender_host = config.PRERENDER_CONFIG['HOST']
prerender_timeout = config.PRERENDER_CONFIG['TIMEOUT']

def clear_cache(cache_key):
	if not cache_key:
		log.warn('prerender|clear_cache,empty_url')
		return False
	params = {
		'url': cache_key
	}
	request_url = prerender_host + '/clear_cache'
	start = time.time()
	response = requests.request('GET', request_url, params=params, timeout=prerender_timeout)
	elapsed = int(time.time() - start)
	if not response or response.status_code != 200:
		log.warn('prerender|elapsed=%s,clear_cache_failed,request_url=%s', elapsed, response.url)
		return False
	log.info('prerender|elapsed=%s,clear_cache_success,request_url=%s', elapsed, response.url)
	return True

def prerender(url):
	user_agents = {
		'mobile': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
		'desktop': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
	}
	result = True
	for key, user_agent in list(user_agents.items()):
		result = result & render(url, user_agent)
	return result

def render(url, user_agent):
	if not url:
		log.warn('prerender|render,empty_url')
		return False
	params = {
		'url': url
	}
	request_url = prerender_host + '/render'
	start = get_timestamp_ms()
	headers = {
		'User-Agent': user_agent
	}
	response = requests.request('GET', request_url, params=params, timeout=prerender_timeout, headers=headers)
	elapsed = get_timestamp_ms() - start
	if not response or response.status_code != 200:
		log.warn('prerender|elapsed=%s,render_failed,request_url=%s,status_code=%s,response_text=%s', elapsed, response.url, response.status_code, response.text)
		return False
	log.info('prerender|elapsed=%s,render_success,request_url=%s', elapsed, response.url)
	return True
