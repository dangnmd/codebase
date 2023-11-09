import requests
from common.logger import log
from common.jsonutils import *
from common.utils import get_timestamp_ms

class TraduoraClient(object):

	def __init__(self, config):
		self._host = config['host']
		self._client_id = config['client_id']
		self._client_secret = config['client_secret']
		self._project_id = config['project_id']
		self._timeout = config['timeout']
		self._access_token = None

	def authorize(self):
		url = self._host + '/api/v1/auth/token'
		response = None
		request_data = {
			"grant_type": "client_credentials",
			"client_id": self._client_id,
			"client_secret": self._client_secret
		}
		start = get_timestamp_ms()
		try:
			response = requests.post(url, data=request_data, timeout=self._timeout)
			elapsed = int(get_timestamp_ms() - start)
			if response.status_code != 200:
				log.warn("request_traduora|elapsed=%s,failed,url=%s,request_data=%s,status_code=%s,response=%s", elapsed, url, request_data, response.status_code, response.text)
			else:
				log.info("request_traduora|elapsed=%s,success,url=%s,request_data=%s", elapsed, url, response.text)
				reply_data = {}
				if response.text != '':
					try:
						reply_data = from_json(response.text)
						self._access_token = reply_data['data']['accessToken']
					except Exception as ex:
						log.exception("request_traduora|exception=%s,url=%s,request_data=%s,status_code=%s,response=%s", ex , url, request_data, response.status_code, response.text)
				return reply_data
		except Exception as error:
			elapsed = int(get_timestamp_ms() - start)
			status_code = None
			if response and response.status_code:
				status_code = response.status_code
			log.exception("request_traduora|exception=%s,elapsed=%s,failed,url=%s,request_data=%s,status_code=%s,response=%s", error, elapsed, url, request_data, status_code, '')
		return None

	def export(self, locale='en_US', export_format='jsonflat'):
		if not self._access_token:
			self.authorize()
		if not self._access_token:
			log.warn('can_not_get_traduora_access_token')
		url = self._host + ('/api/v1/projects/%s/exports?locale=%s&format=%s' % (self._project_id, locale, export_format))
		response = None
		headers = {
			'Authorization': 'Bearer %s' % self._access_token
		}
		start = get_timestamp_ms()
		try:
			response = requests.get(url, headers=headers, timeout=self._timeout)
			elapsed = int(get_timestamp_ms() - start)
			if response.status_code != 200:
				log.warn("request_traduora_export_fail|elapsed=%s,url=%s,request_data=%s,status_code=%s,response=%s", elapsed, url, response.status_code, response.text)
			else:
				log.info("request_traduora_export_success|elapsed=%s,url=%s,request_data=%s", elapsed, url, response.text)
				reply_data = {}
				if response.text != '':
					try:
						reply_data = from_json(response.text)
					except:
						log.exception("parse_traduora_data_fail|url=%s,request_data=%s,status_code=%s,response=%s", url, response.status_code, response.text)
				return reply_data
		except Exception as error:
			elapsed = int(get_timestamp_ms() - start)
			status_code = None
			if response and response.status_code:
				status_code = response.status_code
			log.exception("request_traduora_export_fail|elapsed=%s,url=%s,status_code=%s,response=%s", elapsed, url, status_code, '')
		return None
