import requests
from common.logger import log
from codebase_lib.managers import setting_manager
from codebase_lib.constants import *
from codebase_lib import config

ACCOUNT_KIT_TIMEOUT = 2.0
FACEBOOK_TIMEOUT = 2.0
GOOGLE_TIMEOUT = 2.0

def get_account_kit_profile(token):
	account_kit_url = setting_manager.get_setting(setting_manager.SettingKey.ACCOUNT_KIT_ENDPOINT,
												setting_manager.SettingKeyDefault.ACCOUNT_KIT_ENDPOINT)
	request_url = account_kit_url + "/v1.3/me"
	request_data = {
		"access_token": token
	}
	try:
		reply = requests.get(request_url, params=request_data, timeout=ACCOUNT_KIT_TIMEOUT)
		reply.raise_for_status()
		reply = reply.json()
		# -------------------
		# verify access token
		# -------------------
		if reply['application']['id'] not in config.SOCIAL_APP_ID['FACEBOOK_APP_ID']:
			log.exception("failed_to_verify_access_token|account_kit_login|url=%s,token=%s", request_url, token)
			return None
	except:
		log.exception("failed_to_request_accountkit_server|url=%s,token=%s", request_url, token)
		return None

	if not reply:
		log.warn("no_response_from_accountkit_server|url=%s,token=%s", request_url, token)
		return None

	# require id, phone.country_prefix, phone.national_number

	if "id" not in reply:
		log.warn("no_social_id_in_accountkit_response|url=%s,token=%s,response=%s", request_url, token, reply)
		return None

	social_profile = {
		"social_id": reply["id"]
	}

	phone = reply.get("phone")
	if not phone:
		log.warn("no_phone_number_in_accountkit_response|url=%s,token=%s,response=%s", request_url, token, reply)
		return None

	country_prefix = phone.get("country_prefix")
	national_number = phone.get("national_number")
	if not country_prefix or not national_number:
		log.warn("no_country_prefix_or_national_number|url=%s,token=%s,response=%s", request_url, token, reply)
		return None

	social_profile["country_prefix"] = country_prefix
	social_profile["national_number"] = national_number
	if country_prefix != "84":
		social_profile["phone_number"] = country_prefix + national_number
	else:
		social_profile["phone_number"] = "0" + national_number

	return social_profile

def get_facebook_profile(token):
	# ----------------------------------
	# verify access token
	# ----------------------------------
	if not verify_facebook_token(token):
		# log inside verify
		return None

	facebook_api_url = "https://graph.facebook.com/v3.0/me"  # use v2.12 instead of outdated v2.10
	# attempt to get phone number - if appname (from header - not now) is in foody setting Foody.API.FB.Non.VerifiedApps
	# decided: not get phone number because facebook will not provide it anyway

	request_data = {
		"fields": "id,name,email,first_name,last_name",
		"access_token": token
	}
	try:
		reply = requests.get(facebook_api_url, params=request_data, timeout=FACEBOOK_TIMEOUT)
		reply.raise_for_status()
		reply = reply.json()
	except:
		log.exception("failed_to_request_facebook_server|url=%s,token=%s", facebook_api_url, token)
		return None

	if not reply:
		log.warn("no_response_from_facebook_server|url=%s,token=%s", facebook_api_url, token)
		return None

	# require id

	if "id" not in reply:
		log.warn("no_social_id_in_facebook_response|url=%s,token=%s,res=%s", facebook_api_url, token, reply)
		return None

	social_profile = {
		"social_id": reply["id"],
		"first_name": reply.get("first_name"),
		"last_name": reply.get("last_name"),
		"full_name": reply.get("name"),
		"email": reply.get("email"),
		"login_type": LoginType.FACEBOOK
	}

	gender = reply.get("gender")
	if gender:
		gender = gender.strip().lower()
		if gender == "male":
			social_profile["gender"] = GenderType.MALE
		elif gender == "female":
			social_profile["gender"] = GenderType.FEMALE

	facebook_api_url += "/picture"
	request_data = {
		"access_token": token,
		"redirect": False,
		"height": 1000,
		"width": 1000
	}
	try:
		reply = requests.get(facebook_api_url, params=request_data, timeout=FACEBOOK_TIMEOUT)
		reply.raise_for_status()
		reply = reply.json()
	except:
		log.exception("failed_to_request_facebook_server|url=%s,request_data=%s", facebook_api_url, request_data)
		reply = None

	profile_picture_url = None
	if reply and ("data" in reply) and ("url" in reply["data"]):
		profile_picture_url = reply["data"]["url"]

	if profile_picture_url:
		social_profile["profile_picture_url"] = profile_picture_url

	return social_profile

def get_google_profile(token):
	# https://developers.google.com/identity/sign-in/web/backend-auth
	# not implement verifying ID token signature

	google_api_url = "https://www.googleapis.com/oauth2/v3/tokeninfo" # can get from setting with key API.Login.Google.Link
	# this url is not suitable for massive validation attempts, maybe using google SDK for python is a better choice
	try:
		request_data = {
			"id_token": token
		}
		response = requests.post(google_api_url, params=request_data, timeout=GOOGLE_TIMEOUT)
		response.raise_for_status()
		response = response.json()
		# --------------------------
		# verify access token
		# --------------------------
		if response['aud'] not in config.SOCIAL_APP_ID['GOOGLE_CLIENT_ID']:
			log.warn("failed_to_verify_access_token|google_login|key=%s,token=%s", response['aud'], token)
			return None
	except Exception as e:
		log.exception("failed_to_request_google_server|url=%s,token=%s|%s", google_api_url, token, e)
		return None

	if response is None:
		log.warn("no_response_from_server|url=%s,token=%s", google_api_url, token)
		return None

	# require sub
	if "sub" not in response: # although google guaranteed sub field is existed in all response, but we must check again
		log.warn("no_social_id_in_google_response|url=%s,token=%s,response=%s", google_api_url, token, response)
		return None

	# not verify iss, azp, aud because of information lacking (client_id)
	# not verify expire time

	# if not grant email scope -> no email
	# if not grant profile scope -> no other info

	social_profile = {
		"social_id": response["sub"],
		"first_name": response.get("family_name"),
		"last_name": response.get("given_name"),
		"full_name": response.get("name"),
		"email": response.get("email"),
		"profile_picture_url": response.get("picture"),
		"locale": response.get("locale")
	}

	return social_profile

def verify_facebook_token(user_access_token):
	"""
		@summary: verify user login via our registered app
	"""
	verify_url = "https://graph.facebook.com/app/?access_token=%s" % (user_access_token)
	try:
		reply = requests.get(verify_url, params=None, timeout=FACEBOOK_TIMEOUT)
		reply.raise_for_status()
		reply = reply.json()
		if reply['id'] in config.SOCIAL_APP_ID['FACEBOOK_APP_ID']:
			return True
		else:
			log.warn("failed_to_verify_access_token|facebook_login|token=%s", user_access_token)
			return False
	except Exception as ex:
		log.exception("failed_to_verify_access_token|facebook_login|url=%s,user_access_token=%s|%s", verify_url, user_access_token, ex)
		return False

def get_social_profile(token, login_type):
	if login_type == LoginType.ACCOUNT_KIT:
		return get_account_kit_profile(token)
	elif login_type == LoginType.FACEBOOK:
		return get_facebook_profile(token)
	elif login_type == LoginType.GOOGLE:
		return get_google_profile(token)
	else:
		return None
