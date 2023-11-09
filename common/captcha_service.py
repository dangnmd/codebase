import uuid
import urllib.request, urllib.parse, urllib.error
from .logger import log
import requests

CAPTCHA_SERVICE_IMAGE_URI = 'http://captcha.garena.com/image?key=%s'
CAPTCHA_SERVICE_VERIFY_URI = 'http://captcha.garena.com/api/verify'
CAPTCHA_SERVICE_TIMEOUT = 5

def generate_captcha_uri(ip=None):
	uri = CAPTCHA_SERVICE_IMAGE_URI % uuid.uuid4().hex
	if ip is not None:
		uri += '&ip=' + urllib.parse.quote(ip)
	return uri

def check_captcha_valid(captcha_key, captcha, ip=None):
	try:
		params = {'key': captcha_key, 'captcha': captcha}
		if ip is not None:
			params['ip'] = ip
		captcha = requests.get(CAPTCHA_SERVICE_VERIFY_URI, params=params, timeout=CAPTCHA_SERVICE_TIMEOUT).json()
	except:
		log.exception('error_captcha_service|key=%s,captcha=%s', captcha_key, captcha)
		return False
	if captcha['result'] != 0:
		return False
	return True
