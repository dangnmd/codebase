import time
import os
import hashlib
import hmac
import requests
import mimetypes

from common.jsonutils import from_json, to_json
from common.utils import get_timestamp, get_timestamp_ms, to_bytes
from common.logger import log
from codebase_lib import config
from codebase_lib.managers.cache_manager import simple_cache_data, CACHE_KEY_VNG_CLOUD_AUTHENTICATION
from codebase_lib.managers import faktory_manager
from codebase_lib.constants import FaktoryJobType, SyncMediaType

class MediaAPI(object):
	REQUEST_TIMEOUT = 30

	def __init__(self, media_setting):
		self._upload_url = media_setting['upload_url']
		self._access_key = media_setting['access_key']

	def _gen_header(self):
		return {
			# 'Origin': 'http://www.foody.vn',
		}

	def request(self, api, request_data, files, signature_data):
		headers = self._gen_header()
		url = self._upload_url + api
		signature = hmac.new(bytearray(self._access_key, 'utf-8'), msg=bytearray(signature_data, 'utf-8'), digestmod=hashlib.sha256).hexdigest()
		response = None
		try:
			start = time.time()
			request_data['token'] = signature
			response = requests.post(url, data=request_data, files=files, headers=headers, timeout=MediaAPI.REQUEST_TIMEOUT)
			elapsed = int(time.time() - start)
			if response.status_code != 200:
				log.warn("request_media_fail|elapsed=%s,url=%s,request_data=%s,status_code=%s,response=%s", elapsed, url, request_data, response.status_code, response.text)
			else:
				log.info("request_media_success|elapsed=%s,url=%s,request_data=%s", elapsed, url, response.text)
				reply_data = {}
				if response.text != '':
					try:
						reply_data = from_json(response.text)
					except:
						log.exception("parse_media_data_fail|url=%s,header=%s,request_data=%s,status_code=%s,response=%s", url, headers, request_data, response.status_code, response.text)
				return reply_data
		except Exception as error:
			status_code = None
			if response and response.status_code:
				status_code = response.status_code
			log.exception("request_media_fail|url=%s,header=%s,request_data=%s,status_code=%s,response=%s", url, headers, request_data, status_code, '')
		return None


# sync_media_faktory_client = faktory_manager.FaktoryClient(FaktoryJobType.SYNC_MEDIA)
#
# def add_to_clound(image_id):
# 	sync_data = {
# 		'type': SyncMediaType.CREATING,
# 		'image_id': image_id
# 	}
# 	sync_to_cloud(**sync_data)
#
# def remove_from_cloud(local_path):
# 	sync_data = {
# 		'type': SyncMediaType.DELETING,
# 		'path': local_path
# 	}
# 	sync_media_faktory_client.add_queues([[sync_data, ]])
# 	return
#
# def sync_to_cloud(**sync_data):
# 	sync_media_faktory_client.add_queues([[sync_data, ]])


media_api_client = MediaAPI(config.MEDIA_CONFIG)


def upload_file(media_folder, sub_folder, file_data, file_name, object_id=0, user_id=0, os='_', app_id=1):
	url = "api/v1/upload_image"
	request_timestamp = get_timestamp()
	signature_data = '%s%s%s%s%s%s%s' % (media_folder or '_', sub_folder or '_', object_id or 0, file_name or '_', user_id or 0, os or '_', request_timestamp or 0)

	request_data = {
		'folder': media_folder,
		'sub_folder': sub_folder,
		'user_id': user_id,
		'o_id': object_id,
		'filename': file_name,
		'app_id': app_id,
		'os': os,
		'timestamp': request_timestamp
	}
	files = {'file': (file_name, file_data)}
	response = media_api_client.request(url, request_data, files=files, signature_data=signature_data)
	if not response or response['error_code']:
		log.warn('upload_file_to_media_failed|response=%s', response)
		return ""
	# from codebase_lib.managers.media_manager import add_sync_cloud_queue
	# sync_data = {
	# 	'type': SyncMediaType.CREATING,
	# 	'image_id': response['image_id']
	# }
	# add_sync_cloud_queue(sync_data)
	return response.get("filename")

def remove_file(media_folder, sub_folder, file_name, object_id=0, user_id=0, os='_', app_id=1):
	url = "api/v1/delete_image"
	request_timestamp = get_timestamp()
	signature_data = '%s%s%s%s%s%s%s' % (media_folder or '_', sub_folder or '_', object_id or 0, file_name or '_', user_id or 0, os or '_', request_timestamp or 0)

	request_data = {
		'folder': media_folder,
		'sub_folder': sub_folder,
		'user_id': user_id,
		'o_id': object_id,
		'filename': file_name,
		'app_id': app_id,
		'os': os,
		'timestamp': request_timestamp
	}
	response = media_api_client.request(url, request_data, files=None, signature_data=signature_data)
	if response and response['success'] and response.get('path'):  # remove from cloud
		from codebase_lib.managers.media_manager import add_sync_cloud_queue
		sync_data = {
			'type': SyncMediaType.DELETING,
			'path': response['path']
		}
		add_sync_cloud_queue(sync_data)
	return response['success']


_DEFAULT_TIMEOUT = 10


class CloudStorage(object):
	def __init__(self, config):
		self.config = config
		self.default_timeout = config.get('default_timeout', _DEFAULT_TIMEOUT)

	def auth(self):
		return

	def create_container(self, name):
		return

	def upload_object(self, container, object_name, object_type, file_data):
		return

	def delete_object(self, container, object_name):
		return

	def get_object(self, container, object_name):
		return

SUCCESS_STATUS_CODES = [201]
DELETED_STATUS_CODES = [204]
GET_STATUS_CODES = [200]
class VNGCloudStorage(CloudStorage):
	def __init__(self, config):
		CloudStorage.__init__(self, config)
		self.authentication_url = config['authentication_url']
		self.username = config['username']
		self.password = config['password']
		self.project_id = config['project_id']
		self.url = ''
		self.container = config['container']

	def _request(self, url, method, **params):
		start_time = get_timestamp_ms()
		try:
			params['timeout'] = self.default_timeout
			expected_status_codes = params.pop('expected_status_codes', None)
			response = requests.request(method, url, **params)
			elapsed = get_timestamp_ms() - start_time
			if not expected_status_codes:
				expected_status_codes = SUCCESS_STATUS_CODES
			if 'data' in params and isinstance(params['data'], bytes):
				params.pop('data')
			if response.status_code not in expected_status_codes:
				log.warn("request_vng_cloud_fail|elapsed=%s,url=%s,method=%s,params=%s,status_code=%s", elapsed, url, method, params, response.status_code)
				return None
			log.info("request_vng_cloud_success|elapsed=%s,url=%s,method=%s,params=%s,status_code=%s", elapsed, url, method, params, response.status_code)
			return response
		except Exception as error:
			elapsed = int(time.time() - start_time)
			log.exception("request_vng_cloud_exception|url=%s,method=%s,params=%s,error=%s", elapsed, url, method, params, str(error))
			raise error
		return None

	@simple_cache_data(lambda cache_prefix, self: cache_prefix, **CACHE_KEY_VNG_CLOUD_AUTHENTICATION)
	def get_auth_tokens(self):
		request_body = {
			"auth": {
				"identity": {
					"methods": [
						"password"
					],
					"password": {
						"user": {
							"domain": {
								"name": "default"
							},
							"name": self.username,
							"password": self.password
						}
					}
				},
				"scope": {
					"project": {
						"domain": {
							"name": "default"
						},
						"id": self.project_id
					}
				}
			}
		}
		headers = {'Content-Type': 'application/json'}
		params = {
			'json': request_body,
			'headers': headers
		}
		url = self.authentication_url
		reply = self._request(url, 'POST', **params)
		if not reply:
			return None
		url = ''
		reply_data = from_json(reply.content)
		if not reply_data:
			return None
		catalogs = reply_data['token']['catalog']
		if not catalogs:
			return None
		for catalog in catalogs:
			if catalog['type'] != 'object-store':
				continue
			for endpoint in catalog['endpoints']:
				if endpoint['interface'] != 'public':
					continue
				url = endpoint['url']
				break
		if not url:
			return None
		result = {
			'auth_token': reply.headers['X-Subject-Token'],
			'url': url
		}
		return result

	def upload_object(self, binary_file, file_name):
		auth_tokens = self.get_auth_tokens()
		if not auth_tokens:
			return False
		url = '{}/{}/{}'.format(auth_tokens['url'], self.container, file_name)
		auth_token = auth_tokens['auth_token']
		mime_type, encoding = mimetypes.guess_type(file_name)
		headers = {
			'X-Auth-Token': auth_token,
			'Content-Type': mime_type
		}
		params = {
			'headers': headers,
			'data': binary_file
		}
		response = self._request(url, 'PUT', **params)
		return response.status_code in SUCCESS_STATUS_CODES

	def delete_object(self, file_name):
		auth_tokens = self.get_auth_tokens()
		if not auth_tokens:
			return False
		url = '{}/{}/{}'.format(auth_tokens['url'], self.container, file_name)
		auth_token = auth_tokens['auth_token']
		headers = {
			'X-Auth-Token': auth_token
		}
		params = {
			'headers': headers,
			'expected_status_codes': DELETED_STATUS_CODES
		}
		response = self._request(url, 'DELETE', **params)
		if not response:
			return False
		return response.status_code in DELETED_STATUS_CODES

	def get_object(self, file_name):
		auth_tokens = self.get_auth_tokens()
		if not auth_tokens:
			return False
		url = '{}/{}/{}'.format(auth_tokens['url'], self.container, file_name)
		auth_token = auth_tokens['auth_token']
		headers = {
			'X-Auth-Token': auth_token
		}
		params = {
			'headers': headers,
			'expected_status_codes': GET_STATUS_CODES
		}
		response = self._request(url, 'GET', **params)
		if not response:
			return False
		if response.status_code not in GET_STATUS_CODES:
			return False
		return to_bytes(response.content)

