import requests
import json
from common.logger import log
import time

class FBClient(object):

	def __init__(self, config):
		self.app_id = config['APP_ID']
		self.app_secret = config['APP_SECRET']
		self.graph_endpoint = config['GRAPH_ENDPOINT']

	def scrape_url(self, url):
		params = {
			'scrape': True,
			'id': url,
			'access_token': "%s|%s" % (self.app_id, self.app_secret)
		}
		try:
			start = time.time()
			response = requests.request('POST', self.graph_endpoint, params=params, timeout=20)
			elapsed = int(time.time() - start)
			if response.status_code != 200:
				log.warn('fb_scrape_failed|elapsed=%s,url=%s,status_code=%s,response_text=%s', elapsed, url, response.status_code, response.text)
				return None
			if response.text:
				log.info('fb_scrape_success|elapsed=%s,url=%s,status_code=%s,response_text=%s', elapsed, url, response.status_code, response.text)
				return json.loads(response.text)
			return {}
		except Exception as exception:
			log.exception('fb_scrape_exception|url=%s,error=%s', url, exception)
			return None
