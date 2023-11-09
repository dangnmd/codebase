import os


class ConfigVarTypeConverter(object):
	STRING = str
	INTEGER = int
	FLOAT = float
	HEX = staticmethod(lambda x: x.decode('hex'))

class ConfigVarInfo(object):
	def __init__(self, var_name, var_type_converter=ConfigVarTypeConverter.STRING, required=True, default=None):
		self.var_name = var_name
		self.var_type_converter = var_type_converter
		self.required = required
		self.default = default
		self.cached = None
		self.has_cache = False

	def __get__(self, instance, owner):
		if self.has_cache:
			return self.cached

		var_name = self.var_name
		if var_name not in os.environ:
			if self.required:
				raise Exception("required env var not found: %s" % var_name)
			else:
				return self.default

		raw_value = os.environ[var_name]
		try:
			value = self.var_type_converter(raw_value)
		except:
			raise Exception("convert config var type failed: var_name=%s, type=%s" % (self.var_name, self.var_type_converter))

		self.cached = value
		self.has_cache = True
		return self.cached


class Config(object):
	REQUEST_SIGNATURE_KEY = ConfigVarInfo(
		var_name='REQUEST_SIGNATURE_KEY',
		var_type_converter=ConfigVarTypeConverter.STRING
	)
	OTP_TOKEN_SECRET_KEY = ConfigVarInfo(
		var_name='OTP_TOKEN_SECRET_KEY',
		var_type_converter=ConfigVarTypeConverter.STRING
	)
	OTP_AUTH_CODE_SECRET_KEY = ConfigVarInfo(
		var_name='OTP_AUTH_CODE_SECRET_KEY',
		var_type_converter=ConfigVarTypeConverter.STRING
	)
	LOGIN_TOKEN_SECRET_KEY = ConfigVarInfo(
		var_name='LOGIN_TOKEN_SECRET_KEY',
		var_type_converter=ConfigVarTypeConverter.HEX
	)

class TestConstant(object):
	LIVE_SAMPLE_ACCOUNT = ConfigVarInfo(
		var_name='LIVE_SAMPLE_ACCOUNT',
		required=False,
		default='',
	)
	LIVE_SAMPLE_PASSWORD = ConfigVarInfo(
		var_name='LIVE_SAMPLE_PASSWORD',
		required=False,
		default='',
	)
	LIVE_ACCOUNTANT_ACCOUNT = ConfigVarInfo(
		var_name='LIVE_ACCOUNTANT_ACCOUNT',
		required=False,
		default='',
	)
	LIVE_ACCOUNTANT_PASSWORD = ConfigVarInfo(
		var_name='LIVE_ACCOUNTANT_PASSWORD',
		required=False,
		default='',
	)
