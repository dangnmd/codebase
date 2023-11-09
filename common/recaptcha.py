import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error
import sys

API_SSL_SERVER = "https://www.google.com/recaptcha/api"
API_SERVER = "http://www.google.com/recaptcha/api"
VERIFY_SERVER = "www.google.com"

class RecaptchaResponse(object):
	def __init__(self, is_valid, error_code=None):
		self.is_valid = is_valid
		self.error_code = error_code

def submit(recaptcha_challenge_field,
			recaptcha_response_field,
			private_key,
			remoteip):
	"""
	Submits a reCAPTCHA request for verification. Returns RecaptchaResponse
	for the request

	recaptcha_challenge_field -- The value of recaptcha_challenge_field from the form
	recaptcha_response_field -- The value of recaptcha_response_field from the form
	private_key -- your reCAPTCHA private key
	remoteip -- the user's ip address
	"""
	try:
		if not (recaptcha_response_field and recaptcha_challenge_field and
				len(recaptcha_response_field) and len(recaptcha_challenge_field)):
			return RecaptchaResponse(is_valid=False, error_code='incorrect-captcha-sol')


		def encode_if_necessary(s):
			if isinstance(s, str):
				return s.encode('utf-8')
			return s

		params = urllib.parse.urlencode({
				'privatekey': encode_if_necessary(private_key),
				'remoteip': encode_if_necessary(remoteip),
				'challenge': encode_if_necessary(recaptcha_challenge_field),
				'response': encode_if_necessary(recaptcha_response_field),
				})

		request = urllib.request.Request(
			url="http://%s/recaptcha/api/verify" % VERIFY_SERVER,
			data=params,
			headers={
				"Content-type": "application/x-www-form-urlencoded",
				"User-agent": "reCAPTCHA Python"
				}
			)

		httpresp = urllib.request.urlopen(request)

		return_values = httpresp.read().splitlines()
		httpresp.close()

		return_code = return_values[0]

		if return_code == "true":
			return RecaptchaResponse(is_valid=True)
		else:
			return RecaptchaResponse(is_valid=False, error_code=return_values[1])
	except:
		return RecaptchaResponse(is_valid=False, error_code=sys.exc_info()[1])
