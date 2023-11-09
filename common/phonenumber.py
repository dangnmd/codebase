import copy
import phonenumbers
from common.enum_type import EnumBase
from common.convert import vn_old_phone_to_new_phone

VIETNAM_LANDLINE_AREA_CODES = {
	'203', '204', '205', '206', '207', '208', '209', '210', '211', '212', '213', '214', '215', '216', '218', '219',
	'220', '221', '222', '225', '226', '227', '228', '229', '232', '233', '234', '235', '236', '237', '238', '239',
	'242', '243', '244', '245', '2462', '2463', '2466', '2471', '2473', '248', '251', '252', '254', '255', '256',
	'257', '258', '259', '260', '261', '262', '263', '269', '270', '271', '272', '273', '274', '275', '276', '277',
	'282', '283', '284', '285', '2862', '2863', '2866', '2871', '2873', '290', '291', '292', '293', '294', '296',
	'297', '299'
}

VIETNAM_MOBILE_OPERATOR_CODES = {
	'32', '33', '34', '35', '36', '37', '38', '39', '52', '56', '58', '59', '70', '76', '77', '78', '79', '81', '82',
	'83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '96', '97', '98', '99'
}

VIETNAM_DEPRECATED_MOBILE_OPERATOR_CODES = {
	'120', '121', '122', '123', '124', '125', '126', '127', '128', '129', '162', '163', '164', '165', '166', '167',
	'168', '169', '186', '188', '199'
}

class PhoneNumberType(EnumBase):
	LANDLINE = 1
	MOBILE = 2

def _split_national_number_by_prefix_codes(national_number, prefix_code_set):
	for prefix_len in range(2,5):
		prefix = national_number[:prefix_len]
		if prefix in prefix_code_set:
			if prefix_len > 3:
				return True, (prefix[:3], national_number[3:])
			return True, (prefix, national_number[prefix_len:])
	return False, None

def parse_vietnam_phone(national_number):
	if not national_number:
		return None
	# assume all characters are digits
	is_deprecated = False
	is_landline = False
	phone_number_type = None
	is_mobile, phone_parts = _split_national_number_by_prefix_codes(national_number, VIETNAM_MOBILE_OPERATOR_CODES)
	if not is_mobile:
		is_mobile, phone_parts = _split_national_number_by_prefix_codes(
			national_number, VIETNAM_DEPRECATED_MOBILE_OPERATOR_CODES)
		if is_mobile:
			is_deprecated = True
	if not is_mobile:
		is_landline, phone_parts = _split_national_number_by_prefix_codes(national_number, VIETNAM_LANDLINE_AREA_CODES)
	if is_mobile:
		phone_number_type = PhoneNumberType.MOBILE
	elif is_landline:
		phone_number_type = PhoneNumberType.LANDLINE
	if not phone_number_type:
		return None
	national_number_len = len(national_number)
	if phone_number_type == PhoneNumberType.LANDLINE and national_number_len != 10:
		return None
	if phone_number_type == PhoneNumberType.MOBILE:
		if not is_deprecated and national_number_len != 9:
			return None
		if is_deprecated and national_number_len != 10:
			return None

	formatted_national_number = None
	if phone_number_type == PhoneNumberType.MOBILE and is_deprecated:
		formatted_national_number = vn_old_phone_to_new_phone(national_number, no_prefix=True)
	if not formatted_national_number:
		formatted_national_number = copy.copy(national_number)

	parse_result = {
		"type": phone_number_type,
		"is_deprecated": is_deprecated,
		"formatted": formatted_national_number,
	}
	if phone_number_type == PhoneNumberType.LANDLINE:
		parse_result["area_code"] = phone_parts[0]
	elif phone_number_type == PhoneNumberType.MOBILE:
		parse_result["operator_code"] = phone_parts[0]

	return parse_result

def get_country_from_country_prefix(country_prefix):
	return phonenumbers.region_code_for_country_code(int(country_prefix))
