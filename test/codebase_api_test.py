# -*- coding: utf-8 -*-
import hashlib
import random
import time
import unittest
from datetime import datetime
from Crypto.Cipher import AES
import os
os.environ['PROJECT_NAME'] = 'codebase_api'  # use for config
from .test_common import *
from codebase_lib.constants import *

CODEBASE_API_URL = TEST_CODEBASE_API_URL

if TEST_ENV == RunningEnvironment.DEVELOPMENT:
	CODEBASE_API_URL = "http://0.0.0.0:5001"

if TEST_ENV == RunningEnvironment.STAGING:
	CODEBASE_API_URL = STAGING_CODEBASE_API_URL
elif TEST_ENV == RunningEnvironment.PRODUCTION:
	CODEBASE_API_URL = LIVE_CODEBASE_API_URL

if TEST_ENV in (RunningEnvironment.DEVELOPMENT, RunningEnvironment.TESTING):
	ACCESS_KEY = TEST_MERCHANT_ACCESS_KEYS['CODEBASE_API']
else:
	ACCESS_KEY = LIVE_MERCHANT_ACCESS_KEYS['CODEBASE_API']

AES_BLOCK_SIZE = 16
AES_CBC_IV = '\0' * AES_BLOCK_SIZE

CODEBASE_TEST_URL = CODEBASE_API_URL + "/s2s/test"


def aes_cbc_encrypt(data, key):
	return AES.new(key, AES.MODE_CBC, AES_CBC_IV).encrypt(data)

def pad(s):
	return s + (32 - len(s) % 32) * chr(32 - len(s) % 32)

def request_service_api(url, data, user_token='', method="POST", files=None, client_type=ClientType.IOS):
	access_key = ACCESS_KEY
	return request_api(url, data, access_key, user_token, MERCHANT_ID, method, files, client_type)


class PaymentSmokeTest(unittest.TestCase):
	def test_api(self):
		result_code, reply = request_service_api(CODEBASE_TEST_URL, None, method='GET')
		print(reply)
		self.assertEqual(result_code, Result.SUCCESS)

if __name__ == "__main__":
	unittest.main()
