# coding=utf-8
import re
import base64
import os
import string
import random
from datetime import datetime
from common.utils import api_response, IS_DJANGO_APP, get_timestamp_ms
from common.geo_utils import *
from common import jsonutils
from common.logger import log
from codebase_lib import config
from .constants import *
from codebase_lib.managers import app_manager, setting_manager
import unidecode
import json
import hashlib
from codebase_lib.google_service import *
from bs4 import BeautifulSoup
from urllib.request import urlopen
from tld import get_tld
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


REGEX_EMAIL = re.compile(r'^[\w\-+.%]+@[\w\-.]+\.\w+$')
REGEX_PHONE_NUMBER = re.compile(r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$')


def ensure_str(potential_unicode_string):
	if isinstance(potential_unicode_string, bytes):
		potential_unicode_string = potential_unicode_string.decode('utf-8')
	return potential_unicode_string

if hasattr(config, 'GEOIP_PATH'):
	if os.path.isfile(config.GEOIP_PATH):
		init_geo(config.GEOIP_PATH, GeoLibType.IP2LOCATION)
	else:
		log.warn("geoip_file_not_found|file=%s", config.GEOIP_PATH)

def api_response_data(result_code, reply=None):
	if IS_DJANGO_APP:
		from django import http
		response = http.HttpResponse(jsonutils.to_json({"result": result_code, "reply": reply}))
		response['content-type'] = 'application/json; charset=utf-8'
		#response['X_METRIPRESULT_CODE'] = result_code
		return response
	else:
		return api_response({"result": result_code, "reply": reply})

def api_response_error_params(*args):
	return api_response_data(Result.ERROR_PARAMS)

def get_account_type(account):
	if re.match(REGEX_EMAIL, account):
		return AccountType.ACCOUNT_TYPE_EMAIL
	else:
		return AccountType.ACCOUNT_TYPE_USERNAME

def get_request_location(location):
	result = {
		'lat': 0,
		'lng': 0
	}
	if not location:
		return result
	try:
		points = location.split(':')
		result['lat'] = float(points[0])
		result['lng'] = float(points[1])
	except:
		return result
	return result

def get_request_ip(request):
	if not getattr(request, 'META'):
		return ''
	ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
	# Note: HTTP_X_FORWARDED_FOR might be a list of addresses!
	# NOTE: We only trust the LAST address because it's the proxy address. All IPs before the last one can be mocked by sender.
	if ',' in ip:
		ip = [x for x in [x.strip() for x in ip.split(',')] if x][-1]
	return ensure_str(ip)

def get_local_public_ip():
	from requests import get
	try:
		ip = get('https://api.ipify.org').text
		return ip
	except Exception as ex:
		log.exception('get_local_public_ip|failed,ex=%s', ex)

def get_image_url(image_file_name, id, width, height, main_folder, sub_folder, gender, frefix, is_hr=False):
	if not image_file_name:
		return ""

	if image_file_name.lower().startswith('http://') or image_file_name.lower().startswith(
			'https://') or image_file_name.lower().startswith('//'):
		return image_file_name
	else:
		if width == 0 and height == 0:
			if sub_folder:
				size_folder = sub_folder + "/" + frefix + "/"
			else:
				size_folder = frefix + "/"
		elif width > 0:
			if height == 0:
				size_folder = frefix + str(width)
			else:
				size_folder = frefix + str(width) + "x" + str(height) + "/"
				if frefix != 's' or is_hr:
					size_folder = sub_folder + '/' + size_folder
		else:
			size_folder = frefix + str(height)

		if id:
			folder_id = int(round(id / 10000))
			return "%s%s/g%s/%s/%s%s" % (config.MEDIA_CONFIG['download_url'], main_folder, folder_id, id, size_folder, image_file_name)
		else:
			return "%s%s/%s%s" % (config.MEDIA_CONFIG['download_url'], main_folder, size_folder, image_file_name)

def get_user_gender(gender):
	if gender:
		gender = gender.lower()
		return {
			'f': GenderType.FEMALE,
			'female': GenderType.FEMALE,
			'm': GenderType.MALE,
			'male': GenderType.MALE
		}.get(gender, GenderType.FEMALE)
	return GenderType.FEMALE

def get_image_user_default_url(width, height, gender):
	if get_user_gender(gender) == GenderType.MALE:
		default_avatar = 'user-default-male.png'
	else:
		default_avatar = 'user-default-female.png'
	return get_image_url(default_avatar, 0, width, height, "default", "", gender, "s")

def get_image_user_url(image_file_name, id, width, height, gender):
	if not image_file_name:
		return get_image_user_default_url(width, height, gender)
	if image_file_name.lower().startswith("default-avatar"):
		return get_image_url(image_file_name, None, width, height, 'defaultavatar', None, gender, 's')
	if id == -1:
		return "style/css/images/no-avatar.png"
	elif id == 0:  #admin
		return "style/images/icons/foodylogo.jpg"
	else:
		return get_image_url(image_file_name, id, width, height, "usr", "avt", gender, "c")

def generate_salt(size):
	return to_str(base64.b64encode(os.urandom(size)))

def generate_pass(size):
	random.seed()
	chars = string.ascii_uppercase + string.digits
	return ''.join(random.choice(chars) for _ in range(size))

def is_valid_email(email):
	if not email or len(email) == 0:
		return False
	if not re.match(REGEX_EMAIL, email):
		return False

	return True

def get_gender_type(gender):
	if not gender:
		return GenderType.FEMALE
	gender = gender.lower()
	if gender in GenderTypeChar.MALE:
		return GenderType.MALE
	return GenderType.FEMALE

def verify_white_list(service_id):
	def _verify_white_list(func):
		def _func(request, data):
			url_rule = request.META.get("PATH_INFO", "/")
			request_url = url_rule
			request_ip = get_request_ip(request)
			if not app_manager.is_ip_white_listed(service_id, request_ip, request_url):
				log.warn("ip_not_whitelisted|service_id=%s,request_ip=%s,request_url=%s", service_id, request_ip, request_url)
				return api_response_data(Result.ERROR_NOT_IN_WHITE_LIST)
			return func(request, data)

		return _func

	return _verify_white_list

def verify_internal_account():
	def _verify_email_metrip(func):
		def _func(request, data):
			valid_domain = setting_manager.get_setting(setting_manager.SettingKey.ALLOW_INTERNAL_DOMAIN, setting_manager.SettingKeyDefault.ALLOW_INTERNAL_DOMAIN)
			valid_domain = valid_domain.split(';')
			email = data["email"].strip().lower()
			parts = email.split('@')
			if len(parts) != 2:
				return api_response_data(Result.ERROR_INVALID_EMAIL)
			if parts[1] not in valid_domain:
				log.warn("domain_not_support, email=%s", email)
				return api_response_data(Result.ERROR_INVALID_EMAIL)
			return func(request, data)
		return _func
	return _verify_email_metrip

def get_account_type(account):
	if re.match(REGEX_EMAIL, account):
		return AccountType.ACCOUNT_TYPE_EMAIL
	else:
		return AccountType.ACCOUNT_TYPE_USERNAME

def date_to_timestamp(dt=None, epoch=datetime(1970, 1, 1)):
	"""
	Return timestamp in seconds from given epoch
	@param dt: given python datetime.datetime
	@param epoch: default 1-1-1970
	"""
	if not dt:
		dt = datetime.now()
	td = dt - epoch
	return int(td.total_seconds())

def datetime_to_string(dt, dt_format=DATETIME_FORMAT):
	return dt.strftime(dt_format)

# def date_to_timestamp(dt, epoch=datetime(1970, 1, 1)):
# 	"""
# 	Return timestamp in seconds from given epoch
# 	@param dt: given python datetime.datetime
# 	@param epoch: default 1-1-1970
# 	"""
# 	td = dt - epoch
# 	return td.total_seconds()

def parse_to_begin_date_string(str_from, set_default=True):
	if str_from is not None:
		str_from = str_from.strip()
	if not str_from and set_default:
		str_from = datetime_to_string(datetime.now(), DATE_FORMAT)

	from_date = None
	if str_from:
		str_from += ' 00:00:00'
		try:
			from_date = datetime.strptime(str_from, DATETIME_FORMAT)
		except:
			log.exception("parse_date_string_fail|str_from=%s,set_default=%s", str_from, set_default)
	return from_date

def parse_to_end_date_string(str_to, set_default=True):
	if str_to is not None:
		str_to = str_to.strip()
	if not str_to and set_default:
		str_to = datetime_to_string(datetime.now(), DATE_FORMAT)

	to_date = None
	if str_to:
		str_to += ' 23:59:59'
		try:
			to_date = datetime.strptime(str_to, DATETIME_FORMAT)
		except:
			log.exception("parse_date_string_fail|str_to=%s,set_default=%s", str_to, set_default)
	return to_date

def parse_string_to_date(str_date, dt_format=DATETIME_FORMAT):
	if not str_date:
		return None
	str_date = str_date.strip()
	date_result = None
	try:
		date_result = datetime.strptime(str_date, dt_format)
	except:
		log.exception("parse_string_to_date_fail|str_date=%s", str_date)
	return date_result

def date_to_day_minutes(dt):
	return dt.time().hour * 60 + dt.time().minute

def get_boolean_value(value):
	"""
		get boolean value from django models
	"""
	if value in (b'1', b'\x01', '\x01', '1'):
		return True
	return False

def get_url_rewrite(data):
	"""
		return friendly url
	"""
	data = unidecode.unidecode(data)
	data = data.lower()
	data = data.replace(' ', '-')
	data = re.sub(r"[^a-zA-Z0-9_\-]", '', data)
	data = re.sub(r"-{2,}", "-", data)
	data = re.sub(r"-+$", "", data)
	return data

def format_phone(phone):
	"""
		Remove all spaces in phone
		and make sure phone leading with 0 or +(country_code)
	"""
	if not phone:
		return phone
	phone = phone.replace(' ', '')
	if not phone.startswith('0') and not phone.startswith('+'):
		phone = '0' + phone
	return phone

def call_func_argument(func, argument):
	def _handle():
		func(argument)

	return _handle

def build_message_attribulte(time_to_live):
	message_attributes = {}
	if time_to_live:
		message_attributes['AWS.SNS.MOBILE.APNS.TTL'] = {
			"DataType": "String",
			"StringValue": str(int(time_to_live))
		}
		message_attributes['AWS.SNS.MOBILE.GCM.TTL'] = {
			"DataType": "String",
			"StringValue": str(int(time_to_live))
		}
	return message_attributes

def build_push_payload(message, uri, track_id, notify_type, notify_id, title=''):
	notify_alert = {
		'body': message
	}
	aps_payload_json = {
		"aps": {
			"alert": notify_alert,
			"badge": 1,
			"sound": "default"
			# "content-available": 1
		},
		"uri": uri,
		"track_id": track_id,
		"unread": 1,
		"notify": {
			"type": notify_type,
			"id": notify_id
		}
	}
	fcm_payload_json = {
		"to": '/topics/ANDROID_METRIP',
		"data": {
			"message": message,
			"unread": 1,
			"uri": uri,
			"track_id": track_id,
			"notify": {
				"type": notify_type,
				"id": notify_id
			}
		}
	}
	if title:
		fcm_payload_json['data']['title'] = title
		notify_alert['title'] = title
	fcm_payload = json.dumps(fcm_payload_json)
	aps_payload = json.dumps(aps_payload_json)
	payload = {
		'default': message,
		'APNS': aps_payload,
		'APNS_SANDBOX': aps_payload,
		'GCM': fcm_payload
	}
	return payload

def block2(x):
	v = []
	result = []
	while x > 0:
		v.append(int(x % 2))
		x = int(x / 2)
	for i in range(0, len(v)):
		if v[i] == 1:
			result.append(2**i)
	return result


def md5_hash(*args):
	start_time = get_timestamp_ms()
	hash_data = hashlib.md5(to_bytes(json.dumps(args))).hexdigest()
	end_time = get_timestamp_ms()
	log.info('md5_hash|elapsed=%s,key=%s', end_time - start_time, hash_data)
	return hash_data

def from_extra_data(s):
	result = jsonutils.from_json_safe(s)
	if not result:
		return {}
	return result

def to_extra_data(data):
	if not data:
		return ''
	return to_json_sorted_key(data)

def to_json_sorted_key(data):
	return json.dumps(data, sort_keys=True, separators=(',', ':'))


def _remove_double_char(source, c):
	if not source:
		return ""
	return source.replace(c, "ᵔᵕ").replace("ᵕᵔ", "").replace("ᵔᵕ", c)


def combine_url(*paths):
	root_path = [path for path in paths if "://" in path]
	if not root_path:
		root_path = [path for path in paths if path.startswith('//')]
	root_path = root_path[0] if root_path else None

	result = "/".join([path for path in paths if path and path != root_path])
	result = result.replace("\\", "/")
	result = _remove_double_char(result, "/")

	if root_path:
		root_path = root_path.strip("/")
		result = "/".join([root_path, result])
	return result


def get_webpage_meta_data(url):
	return_meta_data = {}
	meta_dict = {}

	is_valid = validate_url(url)
	if not is_valid and 'http' not in url.lower():
		url = 'http://' + url

	headers = {
		'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Googlebot/2.1 (+http://www.google.com/bot.html) Chrome/15.0.874.121 Safari/537.36',
	}
	response = load_webpage(url, headers=headers)
	if not response:
		response = load_webpage(url)

	if not response or not response.text:
		return None
	soup = BeautifulSoup(response.text)
	for tag in soup.find_all("meta"):
		content = ensure_str(tag.get('content', ''))
		if tag.get('name', '') and not hasattr(meta_dict, tag['name']):
			meta_dict[tag['name']] = content
		if tag.get('property', '') and not hasattr(meta_dict, tag['property']):
			meta_dict[tag['property']] = content

	# OpenGraph Meta Tags
	if meta_dict.get('og:title'):
		return_meta_data['title'] = meta_dict['og:title']
	if meta_dict.get('og:description'):
		return_meta_data['description'] = meta_dict['og:description']
	if meta_dict.get('og:image'):
		return_meta_data['images'] = [meta_dict['og:image']]

	# Basic HTML Meta Tags
	if meta_dict.get('author'):
		return_meta_data['author'] = meta_dict['author']
	if not return_meta_data.get('description') and meta_dict.get('description'):
		return_meta_data['description'] = meta_dict['description']

	tld_res = get_tld(url, as_object=True)
	hostname = tld_res.parsed_url.hostname.upper()
	if not return_meta_data.get('author', ''):
		return_meta_data['author'] = hostname
	if 'YOUTUBE.COM' in hostname:
		return_meta_data['type'] = ExternalArticleType.VIDEO
	else:
		return_meta_data['type'] = ExternalArticleType.BLOG
	return return_meta_data


def load_webpage(url, headers=None):
	try:
		if headers:
			response = requests.get(url, headers=headers)
		else:
			response = requests.get(url)
		if response.status_code != 200:
			raise requests.exceptions.RequestException(
				'Response not OK for {}'.format(url))
	except requests.exceptions.RequestException:
		return None
	return response


def validate_url(url):
	validate = URLValidator()
	try:
		validate(url)
	except ValidationError as e:
		return False
	return True


def to_str(bytes_or_str):
	if isinstance(bytes_or_str, bytes):
		value = bytes_or_str.decode('utf-8')
	else:
		value = bytes_or_str
	return value  # Instance of str


def to_bytes(bytes_or_str):
	if isinstance(bytes_or_str, str):
		value = bytes_or_str.encode('utf-8')
	else:
		value = bytes_or_str
	return value  # Instance of bytes


def is_empty(data):
	if data is None:
		return False
	if type(data) == str and data.strip() == '':
		return True
	if type(data) == list and len(data) == 0:
		return True
	return False

def admin_log(uid, table_name, table_id, log_data):
	log.info("admin_update|uid=%s,table_name=%s,table_id=%s,data=%s", uid, table_name, table_id, log_data)
