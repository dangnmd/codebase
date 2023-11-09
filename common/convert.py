import struct
import socket
import calendar
import time
from datetime import datetime
import pytz
import dateutil.parser
import re
import phonenumbers

_vn_phone_num_prefix_mapping = {
	# Mobifone
	'120': '70',
	'121': '79',
	'122': '77',
	'126': '76',
	'128': '78',
	# Vinaphone
	'123': '83',
	'124': '84',
	'125': '85',
	'127': '81',
	'129': '82',
	# Viettel
	'162': '32',
	'163': '33',
	'164': '34',
	'165': '35',
	'166': '36',
	'167': '37',
	'168': '38',
	'169': '39',
	# Vietnamobile
	'186': '56',
	'188': '58',
	# Gmobile
	'199': '59',
}

_vn_phone_num_prefix_inversion = {value: key for key, value in _vn_phone_num_prefix_mapping.items()}

_number_pattern = re.compile(r'^[0-9]+$')

def ip_to_int(addr):
	return struct.unpack("!I", socket.inet_aton(addr))[0]

ip2int = ip_to_int	#Deprecated!

def int_to_ip(addr):
	return socket.inet_ntoa(struct.pack("!I", addr))

int2ip = int_to_ip	#Deprecated!

def get_tz(country_code):
	try:
		return pytz.timezone(pytz.country_timezones(country_code)[0])
	except:
		return pytz.timezone('Asia/Singapore')

def timestamp_to_string(timestamp, format='%Y-%m-%d %H:%M:%S', country_code=None):	# pylint: disable=redefined-builtin
	if country_code is None:
		dt = datetime.fromtimestamp(int(timestamp))
	else:
		dt = datetime.fromtimestamp(int(timestamp), get_tz(country_code))
	return dt.strftime(format)

time2string = timestamp_to_string	#Deprecated!

def string_to_timestamp(dt_string):
	return datetime_to_timestamp(dateutil.parser.parse(dt_string))

def datetime_to_timestamp(dt):
	return calendar.timegm(dt.utctimetuple())

datetime_to_int = datetime_to_timestamp	#Deprecated!

def timestamp_to_datetime(timestamp, country_code):
	return datetime.fromtimestamp(timestamp, get_tz(country_code))

datetime_from_timestamp = timestamp_to_datetime

def get_current_datetime(country_code):
	now = int(time.time())
	return timestamp_to_datetime(now, country_code)

def strptime_with_tz(dt_string, dt_format, country_code):
	dt = datetime.strptime(dt_string, dt_format)
	return get_tz(country_code).localize(dt)

def vn_old_phone_to_new_phone(phone_num, no_prefix=False):
	# convert valid Vietnam phone number from old format (11 digits) to new format (10 digits)
	# accepted formats: xxxxxxxxxx (first digit != 0), 0xxxxxxxxxx, 84xxxxxxxxxx, +84xxxxxxxxxx
	# return output with the same format as input
	# return input if input is not valid or it is in new format already
	if not phone_num:
		return phone_num
	if not isinstance(phone_num, str): # and not isinstance(phone_num, unicode)
		return phone_num
	if len(phone_num) < 10:
		return phone_num
	prefix = ''
	if not no_prefix:
		if phone_num[0] == '0':
			prefix = '0'
		elif phone_num[:2] == '84':
			prefix = '84'
		elif phone_num[:3] == '+84':
			prefix = '+84'
		else:
			prefix = ''
		# strip prefix
		phone_num = phone_num[len(prefix):]
	if len(phone_num) == 10 and _number_pattern.match(phone_num):
		# convert to new format
		sub_prefix = phone_num[:3]
		if sub_prefix in _vn_phone_num_prefix_mapping:
			# valid mapping
			phone_num = _vn_phone_num_prefix_mapping[sub_prefix] + phone_num[3:]

	return prefix + phone_num

def vn_convert_mobile_phones(phone_num, no_prefix=False):
	# receive phone number and return that phone number in 2 format: 10-digit and 11-digit
	# accepted formats: xxxxxxxxxx (first digit != 0), 0xxxxxxxxxx, 84xxxxxxxxxx, +84xxxxxxxxxx
	# if phone number is invalid or inconvertible, return None
	# return tuple (10-digit phone, 11-digit phone)
	if not phone_num:
		return None, None
	if not isinstance(phone_num, str): # and not isinstance(phone_num, unicode)
		return None, None
	if len(phone_num) < 9:
		return None, None
	prefix = ''
	if not no_prefix:
		if phone_num[0] == '0':
			prefix = '0'
		elif phone_num[:2] == '84':
			prefix = '84'
		elif phone_num[:3] == '+84':
			prefix = '+84'
		else:
			prefix = ''
		# strip prefix
		phone_num = phone_num[len(prefix):]
	if not _number_pattern.match(phone_num):
		return None, None

	if len(phone_num) == 9:
		# currently in 10-digit format
		sub_prefix = phone_num[:2]
		converted_phone_num = phone_num
		if sub_prefix in _vn_phone_num_prefix_inversion:
			converted_phone_num = _vn_phone_num_prefix_inversion[sub_prefix] + phone_num[2:]
		return prefix + phone_num, prefix + converted_phone_num

	if len(phone_num) == 10:
		# currently in 11-digit format
		sub_prefix = phone_num[:3]
		converted_phone_num = phone_num
		if sub_prefix in _vn_phone_num_prefix_mapping:
			converted_phone_num = _vn_phone_num_prefix_mapping[sub_prefix] + phone_num[3:]
		return prefix + converted_phone_num, prefix + phone_num

	return None, None

def split_phone_number(phone_number, default_country=None, support_test_phone=False):
	if not isinstance(phone_number, str):
		return None, None
	phone_number = phone_number.strip()
	if not phone_number:
		return None, None
	if phone_number[0] not in ('0', '+', '('):
		phone_number = '+' + phone_number
	country_code = None
	check_region = True
	if phone_number.startswith('00'):
		if not support_test_phone:
			return None, None
		country_code = '00'
		phone_number = phone_number[2:]
		check_region = False
	elif phone_number.startswith('+00'):
		if not support_test_phone:
			return None, None
		country_code = '00'
		phone_number = phone_number[3:]
		check_region = False
	try:
		phone_obj = phonenumbers.parse(phone_number, region=default_country, _check_region=check_region)
	except phonenumbers.NumberParseException:
		return None, None
	if not country_code:
		if not phone_obj.country_code:
			return None, None
		country_code = str(phone_obj.country_code)
	national_number = str(phone_obj.national_number)
	return country_code, national_number
