import os
import sys
import json
import requests
import hashlib
import hmac
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('../')
from codebase_lib import config
from codebase_lib.constants import RunningEnvironment, ClientType, AppType, Result

from common.utils import get_timestamp
# requests.packages.urllib3.disable_warnings()
from .test_constants import *
import urllib.parse
from urllib.parse import urlencode

TEST_ENV = RunningEnvironment.DEVELOPMENT
TEST_CI_ENABLED = False

TEST_ENVIRONMENTS = (RunningEnvironment.DEVELOPMENT, RunningEnvironment.TESTING)
LIVE_ENVIRONMENTS = (RunningEnvironment.STAGING, RunningEnvironment.PRODUCTION)

CODEBASE_API_URL = TEST_CODEBASE_API_URL
PAYADMIN_API_URL = TEST_PAYADMIN_API_URL

if TEST_ENV == RunningEnvironment.STAGING:
	CODEBASE_API_URL = STAGING_CODEBASE_API_URL
	PAYADMIN_API_URL = STAGING_PAYMENT_ADMIN_API_URL
elif TEST_ENV == RunningEnvironment.PRODUCTION:
	CODEBASE_API_URL = LIVE_CODEBASE_API_URL
	PAYADMIN_API_URL = LIVE_PAYADMIN_API_URL


def request_api(url, data, app_access_key, user_token='', merchant_id='COOKY', method="POST", files=None, client_type=ClientType.IOS, client_version='2300', location=None):
	print('\n','+ REQUEST: ', url)
	query_string = ''
	hash_data = ''
	if method == 'POST':
		if not files:
			hash_data = json.dumps(data)
	else:
		if data:
			query_string = '?' + urlencode(data)
	timestamp = str(get_timestamp())
	url_path = urllib.parse.urlparse(url).path + query_string
	base_string = "%s|%s|%s|%s" % (method, timestamp, url_path, hash_data)
	signature = hmac.new(bytearray(app_access_key, 'utf-8'), msg=bytearray(base_string, 'utf-8'), digestmod=hashlib.sha256).hexdigest()
	headers = {
		'X-Merchant-Id': merchant_id,
		'X-Merchant-Timestamp': timestamp,
		'X-Merchant-Access-Token': signature,
		'Accept-Encoding': 'gzip',
		'content-encoding': 'gzip',
	}

	if method == "POST":
		if files:
			response = requests.post(url, data=data, verify=False, headers=headers, files=files)
		else:
			response = requests.post(url, data=hash_data, verify=False, headers=headers)
	else:
		response = requests.get(url, params=data, verify=False, headers=headers)
	try:
		if response.status_code != 200:
			print(("  REQUEST HTTP ERROR CODE: %s" % response.status_code))
			return None, None
		result = response.json()
		result_code = result["result"]
		result_body = result.get("reply")
		return result_code, result_body
	except Exception as error:
		print(("  REQUEST EXCEPTION: %s" % error.message))
	return None, None

DATE_FORMAT = "%Y-%m-%d"
DAY_MONTH_FORMAT = "%d/%m"
HOUR_SECOND_FORMAT = "%H:%M:%S"
DATETIME_FORMAT = DATE_FORMAT + " " + HOUR_SECOND_FORMAT

SKIP_LIVE_TEST = {
	'condition': TEST_ENV not in TEST_ENVIRONMENTS,
	'reason': 'Skip live test'
}

def datetime_to_string(dt, dt_format=DATETIME_FORMAT):
	return dt.strftime(dt_format)

def is_dev_test():
	return config.RUNNING_ENVIRONMENT in [config.RunningEnvironment.DEVELOPMENT, config.RunningEnvironment.TESTING]
