import requests
import urllib.parse
from codebase_lib.utils import *
from common.jsonutils import *


class SendBirdClient(object):
	def __init__(self, config):
		self.base_url = config['URL']
		self.api_token = config['API_TOKEN']
		self.timeout = config['TIMEOUT']
		self.version = config['VERSION']

	def _gen_headers(self):
		api_headers = {
			'Api-Token': self.api_token,
			'Content-Type': 'application/json, charset=utf8'
		}
		return api_headers

	def _gen_url(self, *segments):
		request_url = combine_url(self.base_url, self.version)
		return combine_url(request_url, *segments)

	def _request(self, **kwargs):
		func_name = kwargs['fn']
		request_url = kwargs['request_url']
		request_data = kwargs.get('request_data')
		request_headers = self._gen_headers()
		request_method = kwargs.get('request_method', 'post').lower()
		response = None
		start = get_timestamp_ms()
		try:
			post_data = None
			if request_data:
				post_data = json.dumps(request_data)
			if request_method == 'get':
				response = requests.get(request_url, headers=request_headers, params=post_data, timeout=self.timeout)
			else:
				if post_data:
					response = requests.request(request_method, request_url, headers=request_headers, data=post_data, timeout=self.timeout)
				else:
					response = requests.request(request_method, request_url, headers=request_headers, timeout=self.timeout)
			elapsed = int(get_timestamp_ms() - start)
			if response.status_code != 200:
				log.warn("request_sendbird|elapsed=%s,failed,fn=%s,url=%s,headers=%s,data=%s,status_code=%s,response=%s", elapsed, func_name, request_url, request_headers, request_data, response.status_code, response.text)
				return None
			log.info("request_sendbird|elapsed=%s,success,fn=%s,url=%s,headers=%s,request_data=%s,response=%s", elapsed, func_name, request_url, request_headers, request_data, response.text)
			reply_data = {}
			if response.text != '':
				reply_data = from_json(response.text)
			return reply_data
		except Exception as error:
			elapsed = int(get_timestamp_ms() - start)
			status_code = None
			if response and response.status_code:
				status_code = response.status_code
			log.exception("request_sendbird|elapsed=%s,exception,fn=%s,err=%s,url=%s,headers=%s,request_data=%s,status_code=%s,response=%s", elapsed,func_name, error, request_url, request_headers, request_data, status_code, '')
		return response

	def create_user(self, **kwargs):
		request_url = self._gen_url('users')
		request_data = kwargs
		return self._request(fn='create_user', request_method='post', request_url=request_url, request_data=request_data)

	def update_user(self, user_id, **kwargs):
		request_url = self._gen_url('users', str(user_id))
		request_data = kwargs
		return self._request(fn='update_user', request_method='put', request_url=request_url, request_data=request_data)

	def view_user(self, user_id):
		request_url = self._gen_url('users', str(user_id))
		return self._request(fn='view_user', request_method='get', request_url=request_url)

	def create_group_channel(self, **kwargs):
		request_url = self._gen_url('group_channels')
		request_data = kwargs
		return self._request(fn='create_group_channel', request_method='post', request_url=request_url, request_data=request_data)

	def update_group_channel(self, channel_url, **kwargs):
		request_url = self._gen_url('group_channels', channel_url)
		request_data = kwargs
		return self._request(fn='update_group_channel', request_method='put', request_url=request_url, request_data=request_data)

	def update_group_channel_metadata(self, channel_url, metadata):
			request_url = self._gen_url('group_channels', channel_url, 'metadata')
			request_data = {
				'metadata': metadata,
				'upsert': True
			}
			return self._request(fn='update_group_channel_metadata', request_method='put', request_url=request_url, request_data=request_data)

	def delete_group_channel(self, channel_url):
		request_url = self._gen_url('group_channels', channel_url)
		return self._request(fn='delete_group_channel', request_method='delete', request_url=request_url)

	def invite_as_group_channel_members(self, channel_url, user_ids):
		request_url = self._gen_url('group_channels', channel_url, 'invite')
		request_data = {
			'user_ids': list(user_ids)
		}
		return self._request(fn='invite_as_group_channel_members', request_method='post', request_url=request_url, request_data=request_data)

	def leave_group_channel(self, channel_url, user_ids):
		request_url = self._gen_url('group_channels', channel_url, 'leave')
		request_data = {
			'user_ids': list(user_ids)
		}
		return self._request(fn='leave_group_channel', request_method='put', request_url=request_url, request_data=request_data)

	def add_user_device_token(self, user_id, token_type, device_token):
		request_url = self._gen_url('users', user_id, 'push', token_type)
		request_data = {}
		if token_type == SendBirdTokenType.APNS:
			request_data['apns_device_token'] = device_token
		elif token_type == SendBirdTokenType.GCM:
			request_data['gcm_reg_token'] = device_token
		return self._request(fn='add_user_device_token', request_method='post', request_url=request_url, request_data=request_data)

	def remove_user_device_token(self, user_id, token_type, device_token):
		request_url = self._gen_url('users', user_id, 'push', token_type, device_token)
		request_data = {}
		if token_type == SendBirdTokenType.APNS:
			request_data['apns_device_token'] = device_token
		elif token_type == SendBirdTokenType.GCM:
			request_data['gcm_reg_token'] = device_token
		return self._request(fn='remove_user_device_token', request_method='delete', request_url=request_url, request_data=request_data)

	def remove_device_token_from_owner(self, token_type, device_token):
		request_url = self._gen_url('push', 'device_tokens', token_type, device_token)
		request_data = {}
		if token_type == SendBirdTokenType.APNS:
			request_data['apns_device_token'] = device_token
		elif token_type == SendBirdTokenType.GCM:
			request_data['gcm_reg_token'] = device_token
		return self._request(fn='remove_device_token_from_owner', request_method='delete', request_url=request_url, request_data=request_data)
