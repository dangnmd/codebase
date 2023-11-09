import random
import requests
from common.logger import log
from common.jsonutils import to_json
from common.utils import ensure_str
import time


class ServiceClientException(Exception):
	pass


class ServiceClientBadStatus(ServiceClientException):
	def __init__(self, request_id, http_status):
		self.request_id = request_id
		self.http_status = http_status

	def __str__(self):
		return "%s - %s" % (self.request_id, self.http_status)


class ServiceClientTimeout(ServiceClientException):
	def __init__(self, request_id):
		self.request_id = request_id

	def __str__(self):
		return str(self.request_id)


class ServiceClientClient(object):
	API_VERSION = "1"
	GENERAL_EXCEPTION_CLS = ServiceClientException
	BAD_STATUS_EXCEPTION_CLS = ServiceClientBadStatus
	TIMEOUT_EXCEPTION_CLS = ServiceClientTimeout
	SERVICE_NAME = "f_service"

	class Result(object):
		SUCCESS = "success"
		ERROR_HEADER = "error_header"
		ERROR_PARAMS = "error_params"
		ERROR_SERVER = "error_server"

	class Api(object):
		pass

	def __init__(self, host, app_id, country='VN', language='vi', timeout=5, retry=3,
				 ignore_info_log=True, merchant_id=None, client_type=None, client_version=None, client_id=None, verify_ssl=None):
		self._host = (host or '').strip(' /')
		self._app_id = app_id
		self._country = country
		self._language = language
		self._timeout = timeout
		self._retry = retry
		self._ignore_info_log = ignore_info_log
		self._session = requests.Session()
		self._max_request_id = (2**64)-1
		self._request_id = None
		self._merchant_id = merchant_id
		self._client_type = client_type
		self._client_version = client_version
		self._client_id = client_id
		self._verify_ssl = verify_ssl

	def _gen_header(self, user_token=None):
		headers = {
			'X-Cooky-Request-Id': str(self._request_id),
			'X-Cooky-Api-Version': self.API_VERSION,
			'X-Cooky-App-Id': str(self._app_id),
			'X-Cooky-Country': self._country,
			'X-Cooky-Language': self._language
		}

		if self._merchant_id:
			headers["X-Merchant-Id"] = self._merchant_id
		if self._client_type is not None:
			headers["X-Cooky-Client-Type"] = self._client_type
		if self._client_version is not None:
			headers["X-Cooky-Client-Version"] = self._client_version
		if self._client_id is not None:
			headers["X-Cooky-Client-Id"] = self._client_id
		if user_token:
			headers["X-Cooky-User-Token"] = user_token
		return headers

	def _request(self, api, data, method, user_token=None):
		self._request_id = random.randint(0, self._max_request_id)
		if not self._ignore_info_log:
			try:
				log_data = data
				if isinstance(log_data, str):
					log_data = ensure_str(log_data)
				log.info(
					"%s_request|host=%s,api=%s,request_id=%s,method=%s,data=%s",
					self.SERVICE_NAME, self._host, api, self._request_id, method, log_data
				)
			except:
				pass
		headers = self._gen_header(user_token)
		timeout = self._timeout

		if self._verify_ssl is not None:
			self._session.verify = self._verify_ssl

		if method == "POST":
			if not isinstance(data, str):
				request_body = to_json(data, ensure_bytes=True)
			else:
				request_body = ensure_str(data)
			response = self._session.post(self._host + api, data=request_body, headers=headers, timeout=timeout)
		else:
			response = self._session.get(self._host + api, params=data, headers=headers, timeout=timeout)
		if response.status_code != 200:
			log.error(
				"%s_request_fail|request_id=%s,status_code=%s,api=%s",
				self.SERVICE_NAME, self._request_id, response.status_code, api
			)
			raise self.BAD_STATUS_EXCEPTION_CLS(self._request_id, response.status_code)

		result = response.json()
		result_code = result["result"]
		result_body = result.get("reply")
		return result_code, result_body

	def request(self, api, data, method="POST", disable_retry=False, user_token=None):
		request_id = random.randint(0, self._max_request_id)
		retry_count = self._retry if not disable_retry else 1
		while retry_count > 0:
			retry_count -= 1
			try:
				start = time.time()
				result_code, result_body = self._request(api, data, method, user_token)
				end = time.time()
				elapsed = int((end - start) * 1000)
				log.info("request_%s_success|elapsed=%s,request_id=%s,status_code=%s,url=%s,request_data=%s", self.SERVICE_NAME, elapsed, request_id, result_code, api, data)
				if retry_count > 0 and result_code == self.Result.ERROR_SERVER:
					log.warn("%s_server_error|request_id=%s,retry_count=%s", self.SERVICE_NAME, self._request_id, retry_count)
				else:
					return result_code, result_body
			except (requests.exceptions.ConnectTimeout, requests.exceptions.Timeout, requests.exceptions.ReadTimeout,
					requests.exceptions.ConnectionError) as error:
				log.exception("%s_request_timeout|request_id=%s,error=%s", self.SERVICE_NAME, self._request_id, error)
				if retry_count <= 0:
					raise self.TIMEOUT_EXCEPTION_CLS(self._request_id)
			except self.BAD_STATUS_EXCEPTION_CLS:
				if retry_count <= 0:
					raise
			except:
				log.exception("%s_request_exception|request_id=%s", self.SERVICE_NAME, self._request_id)
				if retry_count <= 0:
					raise
