import random
import requests
from .logger import log
from .jsonutils import to_json
from .utils import get_timestamp_ms

class ReviewServiceBadStatus(Exception):
	def __init__(self, request_id, http_status):
		self.request_id = request_id
		self.http_status = http_status

	def __str__(self):
		return "%s - %s" % (self.request_id, self.http_status)

class ReviewServiceTimeout(Exception):
	def __init__(self, request_id):
		self.request_id = request_id

	def __str__(self):
		return str(self.request_id)

class ReviewServiceClient(object):
	APP_VERSION = "1"

	class Result(object):
		SUCCESS = "success"
		ERROR_HEADER = "error_header"
		ERROR_PARAMS = "error_params"
		ERROR_SERVER = "error_server"
		ERROR_FORBIDDEN = "error_forbidden"
		ERROR_NOT_IN_WHITE_LIST = "error_not_in_whitelist"

	class Api(object):
		REVIEW_GET_LIKE_STATS = "/s2s/review/get_like_stats"

	def __init__(self, host, app_id, timeout=5, retry=3):
		self._host = host
		self._app_id = app_id
		self._timeout = timeout
		self._retry = retry

		self._request_id = random.randint(0, 10 ** 10)
		self._session = requests.Session()

	def _gen_header(self, app_id):
		return {
			'X-App-Request-Id': str(self._request_id),
			'X-App-Id': str(app_id) if app_id else str(self._app_id),
		}

	def _request(self, api, data, method, app_id=None):
		self._request_id += 1
		log.info("request_review_service|host=%s,api=%s,request_id=%s,method=%s,data=%s", self._host, api, self._request_id, method, data)
		start_time = get_timestamp_ms()
		headers = self._gen_header(app_id)
		timeout = self._timeout
		if method == "POST":
			response = self._session.post(self._host + api, data=to_json(data, ensure_bytes=True), headers=headers, timeout=timeout)
		else:
			response = self._session.get(self._host + api, params=data, headers=headers, timeout=timeout)
		if response.status_code != 200:
			log.error("request_review_service|request_id=%s,status_code=%s,api=%s", self._request_id, response.status_code, api)
			raise ReviewServiceBadStatus(self._request_id, response.status_code)

		result = response.json()
		result_code = result["result"]
		result_body = result.get("reply")
		elapsed = get_timestamp_ms() - start_time
		log.info("request_review_service|elapsed=%s,request_id=%s,status_code=%s,api=%s", elapsed, self._request_id, response.status_code, api)
		return result_code, result_body

	def request(self, api, data, method="POST", disable_retry=False, app_id=None):
		if disable_retry:
			return self._request(api, data, method, app_id)
		else:
			retry_count = self._retry
			while True:
				retry_count -= 1
				try:
					result_code, result_body = self._request(api, data, method, app_id)
					if retry_count > 0 and result_code == ReviewServiceClient.Result.ERROR_SERVER:
						log.warn("get_error_server|request_id=%s,retry_count=%s", self._request_id, retry_count)
					else:
						return result_code, result_body
				except requests.exceptions.ConnectTimeout:
					log.exception("request_review_service|request_id=%s", self._request_id)
					if retry_count == 0:
						raise ReviewServiceTimeout(self._request_id)
				except ReviewServiceBadStatus as error:
					log.exception("request_review_service|request_id=%s,http_code=%s", self._request_id, error.http_status)
					if retry_count == 0:
						raise
				except Exception as error:
					log.exception("request_review_service|request_id=%s", self._request_id)
					if retry_count == 0:
						raise
