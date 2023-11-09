import hashlib
import hmac
from functools import wraps
from .utils import get_timestamp, api_response_data, api_response_error_params, get_request_ip, get_request_location
from .constants import BaseResult
from .logger import log
from .authapiservice import AuthServiceClient
from .service.auth_service_client import auth_api_client
from config import config

def pre_process_user_header():
	def _pre_process_header(func):
		@wraps(func)
		def _func(request, *args, **kwargs):
			data = {}
			if len(args) > 0:
				data = args[0]

			headers = request.META
			try:
				data["app_id"] = int(headers["HTTP_X_COOKY_APP_ID"])
				data["client_type"] = int(headers["HTTP_X_COOKY_CLIENT_TYPE"])
				data["client_version"] = str(headers["HTTP_X_COOKY_CLIENT_VERSION"])
				data["client_id"] = str(headers["HTTP_X_COOKY_CLIENT_ID"])
				data["client_language"] = str(headers.get("HTTP_X_COOKY_CLIENT_LANGUAGE", "en"))
				data["timestamp"] = headers.get("HTTP_X_COOKY_TIMESTAMP")
				data["user_token"] = headers.get("HTTP_X_COOKY_USER_TOKEN")
				data["location"] = get_request_location(headers.get("HTTP_X_LOCATION"))
				data["city_id"] = int(headers.get("HTTP_X_COOKY_CITY_ID", 0))
				data["seller_id"] = int(headers.get("HTTP_X_COOKY_SELLER", 0))
			except Exception as err:
				log.exception("header_invalid|headers=%s", headers)
				return api_response_data(BaseResult.ERROR_HEADER)

			# find ip country
			# country_code_by_ip = geo_ip_to_country(request.META['REMOTE_ADDR'])  # 'ZZ'
			# data['_ip'] = ip_to_int(request.META['REMOTE_ADDR'])
			# data['_country_by_ip'] = country_code_by_ip
			data['request_ip'] = get_request_ip(request)
			url_rule = request.META.get("PATH_INFO", "/")
			data['request_api'] = url_rule
			# if is_maintenance(data['_service_id'], data['_app_type'], data['_request_api']):
			# 	return api_response_data(BaseResult.ERROR_SERVER_MAINTENANCE)
			if len(args) > 0:
				return func(request, *args, **kwargs)
			else:
				return func(request, data, *args, **kwargs)

		return _func

	return _pre_process_header


def verify_user_token(require_login=True):
	def _verify_user_token(func):
		@wraps(func)
		def _func(request, data, *args, **kwargs):
			user_token = data.get('user_token')
			if not user_token:
				log.warn("user_token_not_found|data=%s", data)
				if require_login:
					return api_response_data(BaseResult.ERROR_USER_TOKEN)
				data["uid"] = 0
				return func(request, data, *args, **kwargs)
			app_id = data['app_id']
			request_data = {
				'app_id': app_id,
				'token': user_token,
				'client_version': data['client_version'],
				'client_type': data['client_type']
			}
			result_code, reply = auth_api_client.request(AuthServiceClient.Api.USER_VERIFY_TOKEN, request_data, app_id=app_id)
			if result_code != BaseResult.SUCCESS:
				log.warning('invalid_user_token|app_id=%s,token=%s', app_id, user_token)
				if require_login:
					return api_response_data(result_code)
				else:
					data["uid"] = 0
					return func(request, data, *args, **kwargs)
			data['session'] = {
				'uid': reply['uid'],
				'username': reply['username'],
				'expiry_time': reply['expiry_time']
			}
			data["uid"] = reply['uid']
			return func(request, data, *args, **kwargs)
		return _func
	return _verify_user_token


def get_current_uid(data):
	return data['uid']


def pre_process_merchant_header():
	def _pre_process_header(func):
		@wraps(func)
		def _func(request, *args, **kwargs):
			data = {}
			if len(args) > 0:
				data = args[0]
			headers = request.META
			try:
				data["merchant_id"] = headers.get("HTTP_X_MERCHANT_ID")
				data["access_token"] = headers.get("HTTP_X_MERCHANT_ACCESS_TOKEN")
				data["timestamp"] = headers.get("HTTP_X_MERCHANT_TIMESTAMP")
			except Exception as err:
				log.exception("header_invalid|headers=%s", headers)
				return api_response_data(BaseResult.ERROR_HEADER)
			data['request_ip'] = get_request_ip(request)
			url_rule = request.META.get("PATH_INFO", "/")
			data['request_api'] = url_rule
			if len(args) > 0:
				return func(request, *args, **kwargs)
			else:
				return func(request, data, *args, **kwargs)
		return _func

	return _pre_process_header


def verify_merchant_access_token(ignore_body=False):
	def _verify_access_token(func):
		def _func(request, data, *args, **kwargs):
			if not auth_api_client:
				return func(request, data, *args, **kwargs)
			merchant_id = data['merchant_id']
			access_token = data['access_token']
			if not access_token:
				log.warning('verify_access_token_missing_signature|body=%s', request.body)
				return api_response_data(BaseResult.ERROR_SIGNATURE)
			request_method = request.method
			if ignore_body:
				request_body = ''
			else:
				request_body = request.body.decode('utf-8')
			request_timestamp = data['timestamp']
			base_string = "%s|%s|%s|%s" % (request_method, request_timestamp, request.get_full_path(), request_body)
			request_ip = data['request_ip']
			request_api = data['request_api']
			request_data = {
				'merchant_id': merchant_id,
				'base_string': base_string,
				'access_token': access_token,
				'request_ip': request_ip,
				'request_api': request_api
			}
			result, reply = auth_api_client.request(AuthServiceClient.Api.MERCHANT_VERIFY_ACCESS_TOKEN, request_data)
			if result != BaseResult.SUCCESS:
				app_id = config.AUTH_SERVICE['app_id']
				log.warning('verify_access_token_mismatch|merchant_id=%s,service_id=%s,base_string=%s,signature_header=%s', merchant_id, app_id, access_token, base_string)
				return api_response_data(BaseResult.ERROR_SIGNATURE)
			return func(request, data, *args, **kwargs)
		return _func
	return _verify_access_token
