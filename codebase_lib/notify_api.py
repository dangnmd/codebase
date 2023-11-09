import time
import requests
import json

from common.jsonutils import from_json
from common.logger import log
from codebase_lib import config

class NotifyAPI(object):
	REQUEST_TIMEOUT = 30

	def __init__(self, notify_setting):
		self._url = notify_setting['url']

	def _gen_header(self):
		return {
			# 'Origin': 'http://www.foody.vn',
		}

	def request(self, api, request_data):
		headers = self._gen_header()
		url = self._url + api
		# signature = hmac.new(bytearray(self._access_key, 'utf-8'), msg=bytearray(signature_data, 'utf-8'), digestmod=hashlib.sha256).hexdigest()
		response = None
		try:
			start = time.time()
			# request_data['token'] = signature
			post_data = json.dumps(request_data)
			response = requests.post(url, data=post_data, headers=headers, timeout=NotifyAPI.REQUEST_TIMEOUT)
			elapsed = int(time.time() - start)
			if response.status_code != 200:
				log.warn("request_notify_api_fail|elapsed=%s,url=%s,request_data=%s,status_code=%s,response=%s", elapsed, url, request_data, response.status_code, response.text)
			else:
				reply_data = {}
				if response.text != '':
					try:
						reply_data = from_json(response.text)
					except:
						log.exception("parse_notify_data_fail|url=%s,header=%s,request_data=%s,status_code=%s,response=%s", url, headers, request_data, response.status_code, response.text)
				if reply_data['result']!='success':
					log.warn("request_notify_api_fail|elapsed=%s,url=%s,request_data=%s,status_code=%s,response=%s", elapsed, url, request_data, response.status_code, response.text)
					return reply_data
				log.info("request_notify_api_success|elapsed=%s,url=%s,request_data=%s,status_code=%s,response=%s", elapsed, url, request_data, response.status_code, response.text)
				return reply_data
		except Exception as error:
			status_code = None
			if response and response.status_code:
				status_code = response.status_code
			log.exception("request_notify_fail|url=%s,header=%s,request_data=%s,status_code=%s,response=%s", url, headers, request_data, status_code, '')
		return None


notify_api_client = NotifyAPI(config.NOTIFY_CONFIG)

def add_notify_to_users(receiver_ids, sender_id, action_type, object_type, object_id, uri, message):
	api = '/s2s/add_notify_to_users'
	if not isinstance(object_id, str):
		object_id = str(object_id)
	request_data = {
		'receiver_ids': receiver_ids,
		'sender_id': sender_id,
		'action_type': action_type,
		'object_type': object_type,
		'object_id': object_id,
		'uri': uri,
		'message': message
	}
	notify_api_client.request(api, request_data)

def update_notify_to_users(action_type, object_type, object_id, receiver_ids=None, sender_id=None, uri=None, message=None):
	api = '/s2s/update_notify_to_users'
	if not isinstance(object_id, str):
		object_id = str(object_id)
	request_data = {
		'action_type': action_type,
		'object_type': object_type,
		'object_id': object_id
	}
	if receiver_ids:
		request_data['receiver_ids'] = receiver_ids
	if sender_id:
		request_data['sender_id'] = sender_id
	if uri:
		request_data['uri'] = uri
	if message:
		request_data['message'] = message
	notify_api_client.request(api, request_data)