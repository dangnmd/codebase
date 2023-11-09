import hashlib
from common.crypt import *
from common.buffer_writer import BufferWriter
from common.buffer_reader import BufferReader
from common.convert import ip_to_int
from common.utils import to_str, to_bytes

def verify_password(password_hash, password, verify_code):
	password_hash_to_check = hashlib.sha256(to_bytes(hashlib.sha256(to_bytes(password)).hexdigest() + verify_code)).hexdigest()
	if password_hash_to_check != password_hash:
		return False
	return True

def create_password(raw_password, salt):
	return hashlib.sha1(raw_password + salt).hexdigest()

def encrypt_user_token(uid, username, createtime, expirytime, salt, ip, key):
	ip = ip_to_int(to_str(ip))
	username = to_bytes(username)
	salt = to_bytes(salt)
	random_number = random.randint(0, 0xffffffff)
	writer = BufferWriter('<')
	writer.add_uint32(random_number)
	writer.add_uint32(uid)
	writer.add_uint32(createtime)
	writer.add_uint32(expirytime)
	username_size = len(username)
	writer.add_uint32(username_size)
	writer.add_buffer(username)
	salt_size = len(salt)
	writer.add_uint32(salt_size)
	writer.add_buffer(salt)
	writer.add_uint32(ip)
	padding_size = (len(writer.buffer) + 4) % 16
	if padding_size:
		writer.add_padding(16 - padding_size)
	checksum = 0
	i = 0
	while i < len(writer.buffer):
		checksum ^= struct.unpack_from('<I', writer.buffer, i)[0]
		i += 4
	writer.add_uint32(checksum)
	return aes_cbc_encrypt(writer.buffer, key[0:32]).hex()

def decrypt_user_token(user_token, key):
	try:
		user_token = bytes.fromhex(user_token)
		if len(user_token) % 16 != 0:
			return None
		plain = aes_cbc_decrypt(user_token, key[0:32])
		checksum = 0
		i = 0
		while i < len(plain):
			checksum ^= struct.unpack_from('<I', plain, i)[0]
			i += 4
		if checksum != 0:
			return None
		reader = BufferReader(plain, '<')
		_ = reader.get_uint32()
		uid = reader.get_uint32()
		createtime = reader.get_uint32()
		expirytime = reader.get_uint32()
		username_size = reader.get_uint32()
		username = reader.get_buffer(username_size)
		salt_size = reader.get_uint32()
		salt = reader.get_buffer(salt_size)
		ip = reader.get_uint32()
		return {'uid': uid, 'username': username.decode('utf-8'), 'create_time': createtime, 'expiry_time': expirytime, "salt": salt.decode('utf-8'), "ip": ip}
	except:
		return None

def pad(s):
	return s + (32 - len(s) % 32) * chr(32 - len(s) % 32)

def unpad(s):
	return s[:-ord(s[len(s)-1:])]

def decrypt_aes_password(new_password, key):
	encrypted_pass = aes_cbc_decrypt(new_password.decode('hex'), key[:32])
	return unpad(encrypted_pass)

def encrypt_confirm_password_code(uid, createtime, expirytime, key):
	random_number = random.randint(0, 0xffffffff)
	writer = BufferWriter('<')
	writer.add_uint32(random_number)
	writer.add_uint32(uid)
	writer.add_uint32(createtime)
	writer.add_uint32(expirytime)
	padding_size = (len(writer.buffer) + 4) % 16
	if padding_size:
		writer.add_padding(16 - padding_size)
	checksum = 0
	i = 0
	while i < len(writer.buffer):
		checksum ^= struct.unpack_from('<I', writer.buffer, i)[0]
		i += 4
	writer.add_uint32(checksum)
	return aes_cbc_encrypt(writer.buffer, key[0:32]).encode('hex')
