from hashids import Hashids
from codebase_lib import config
from codebase_lib.constants import *
from codebase_lib.managers import setting_manager
import time
from common.logger import log

def get_id_encoder():
	if 'instance' not in get_id_encoder.__dict__:
		min_length = setting_manager.get_setting_number(setting_manager.SettingKey.HASH_IDS_MIN_LENGTH, setting_manager.SettingKeyDefault.HASH_IDS_MIN_LENGTH)
		salt = config.HASHID_CONFIG["SALT"]
		get_id_encoder.instance = Hashids(salt=salt, min_length=min_length)
	return get_id_encoder.instance

def encode_id(object_type, object_id, encoder=None):
	if not object_id:
		return None
	if not encoder:
		encoder = get_id_encoder()
	variant = config.HASHID_CONFIG["VARIANT_DATA"]
	object_code = encoder.encode(object_type, object_id, variant)
	return object_code

def decode_id(object_code, decoder=None):
	data = decode_raw(object_code, decoder)
	if not data:
		return None
	return data[1]		# (object_type, object_id, variant)

def decode_raw(object_code, decoder=None):
	if not decoder:
		decoder = get_id_encoder()
	data = decoder.decode(object_code)
	return data

def encode_ids(object_type, object_ids):
	if not object_ids:
		return []
	# start = time.time()
	encoder = get_id_encoder()
	# end = time.time()
	# elapsed = int((end - start) * 1000)
	# log.info("encode_ids|get_encoder|elapsed=%s", elapsed)
	# start = time.time()
	object_codes = []
	for object_id in object_ids:
		object_code = encode_id(object_type, object_id, encoder)
		object_codes.append(object_code)
	# end = time.time()
	# elapsed = int((end - start) * 1000)
	# log.info("encode_ids|complete|elapsed=%s", elapsed)
	return object_codes

def decode_ids(object_codes):
	decoder = get_id_encoder()
	ids = []
	for object_code in object_codes:
		object_id = decode_id(object_code, decoder)
		if object_id:
			ids.append(object_id)
	return ids

def encode_list_number(object_type, list_number, encoder=None):
	if not encoder:
		encoder = get_id_encoder()
	variant = config.HASHID_CONFIG["VARIANT_DATA"]
	object_code = encoder.encode(object_type, variant, *list_number)
	return object_code

def use_raw_id_version(data):
	client_type = data["_client_type"]
	client_version = data["_client_version"]
	if client_type == ClientType.IOS and client_version < 1510:
		return True
	if client_type == ClientType.ANDROID and client_version < 1120:
		return True
	if client_type == ClientType.WEB and client_version < 1100:
		return True
	return False


