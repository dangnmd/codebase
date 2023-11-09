import hashlib
import hmac
import json
from .logger import log
import requests

# Need apply access before use these services.

SEND_SMS_URL = 'http://sms.garenanow.com:8600/'
SEND_SMS_TIMEOUT = 10
SEND_EMAIL_URL = 'http://sendgrid.garenanow.com/sendmail'
SEND_EMAIL_KEY = '4190d4fea00aacd9ace0b4b9cdc3e420'
SEND_EMAIL_TIMEOUT = 10

def send_sms(mobile_no, text, source='garena', url=SEND_SMS_URL):
	try:
		response = requests.get(url, params={'number': mobile_no, 'text': text.encode('utf-8'), 'source': source}, timeout=SEND_SMS_TIMEOUT)
		response.raise_for_status()
		result = response.text
		if "Success" in result:
			log.data('send_sms|mobile_no=%s,text=%s', mobile_no, text)
			return True
		else:
			log.warn('send_sms_fail|mobile_no=%s,text=%s,result=%s', mobile_no, text, result)
			return False
	except Exception as ex:
		log.warn('send_sms_exception|mobile_no=%s,text=%s,exception=%s', mobile_no, text, ex, exc_info=True)
		return False

def send_email(from_addr, to_addr, subject, body, split_multi_receivers=True):
	"""
	:param split_multi_receivers:
		When `split_multi_receivers` is True, email_service would treat every receiver as a new email.
		When `split_multi_receivers` is False, email_service would send one email which header contains all receivers in email.
		Default value is True.
	:return: return True when send success otherwise return False.
	"""
	plain = (to_addr + from_addr + subject + body).encode('utf-8')
	sign = hmac.new(SEND_EMAIL_KEY, plain, hashlib.sha1).hexdigest()
	if split_multi_receivers:
		split_multi_receivers = 1
	else:
		split_multi_receivers = 0
	params = {
		'from': from_addr,
		'to': to_addr,
		'subject': subject,
		'body': body,
		'sign': sign,
		'split_multi_receivers': split_multi_receivers,
	}
	try:
		headers = {'content-type': 'application/json'}
		body = json.dumps(params)
		response = requests.post(SEND_EMAIL_URL, data=body, headers=headers, timeout=SEND_EMAIL_TIMEOUT)
		response.raise_for_status()
		result = response.json()
		result_code = result.get('result', 0)
		if result_code == 0:
			log.data('send_email|from=%s,to=%s,subject=%s', from_addr, to_addr, subject)
			return True
		else:
			log.warn('send_email_fail|from=%s,to=%s,subject=%s,result=%s,error=%s', from_addr, to_addr, subject, result_code, result.get('detail', ''))
			return False
	except Exception as ex:
		log.warn('send_email_exception|from=%s,to=%s,subject=%s,exception=%s', from_addr, to_addr, subject, ex, exc_info=True)
		return False
