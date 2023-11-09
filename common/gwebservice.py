# pylint: skip-file
import base64
import random
import string
import os
from Crypto.Cipher import AES

GWS_KEY = '''-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEA3XK9BWuIHIS3R6za4WU/mQ0WlsPD/ErtzSTw2ZmbhI0lyKcQ
Ugk0aRIOaq4vTE+EpRtI6hvhH4AIm+15sWPqxpfuNR0Dvigse+BhuypFsqI+AWiL
dj5RrPSzrLcqWgjE5zSjUG4OmxS4NJJRY9UMNaEhtqsrgrFFj4iMX07bz6Joyp85
CHpGJhmFjPwU60OlUkGKwvs6TeQXUZlH9ypzXkNAhF4uDchTgEX7A/8yrqHzPx7/
r2T0Lww7kp106ACdy9wXTpq5v3tmfNZbZ7K0bEB4g8Ez43Hew1P5b/tabUV4pZL0
LkvDCA78ll8FHeuJjZA3+DKlEgyA2EWTs98VTQIDAQABAoIBAC65evCd08ZQqmtR
KY3NUzHz9QQyojOli69xT/BZ3NqG/aXsuiDVGF3jFW+k+Q3c6Vv8+dGLuGBxH1/n
J3oqXuswO26xhIym5Vvt6DEZpkMewH6DlImKdKlNqGuU6ja9Cu7NyHe8ARDvuj49
cTbjSQQ3z2k/jJqy1L6ITTX+6ZpRgZd9m/Ng5O0GBcoSiUjysfLgs5m5lHWCojL+
ppxqhsWXDM2ejIFGncGok798NNps+OkAM9EwEHcEI7qBo/UEsgXwnmlUvsyBvtq3
7NS/znsJlOT/PfbS3i0gIac6AmA0qh86zN+uC5yl44aY+WpwPqBua6eeKkpk3xAo
LrCRxHECgYEA/689gaRf0ihJ5WpD/cq6XLFwxuu4/CmmNjYpTwol2S3lGnq03RLZ
FhklvMKIkhfuaOLyrHgUWaYZVr2KBUU81qwHTVEZeN6rWPeXTsfgBnpShIYYXqBN
ePyqVDuISs44Lsi74fhSNrqai6ow6GQYlZewcdjS2zVc35G1of/cWNMCgYEA3biv
L49okrATQfBbdl5L6hueqNc8pfrv6EKYcw5SE48fFeHCToorKpaf4kf7GemITldD
29FFwukhyt1rJJI9Kvj6jKN49QZr3xS1d8QY0lOHnRRRLIg3x+VaD7RYOWuHbqs1
MKyzgeKkpWq6EkuaW2ZEQwL6cvzqGsbo1CRqBV8CgYBMNqEf1q5VR3sXbkCMEvTQ
EngqYzNFvuhzelt/2ueDQCHtbawhxa993csY4+evnICNNTDe5gAy5MbiyyasAYJr
/uVCT61HESCEKXEpo3yMkcOtCweSlTfim3XuG7y5h5TJpT4T0mA3PhI5FWb0rnmB
hbCrjtTzUIm5foZkno7AzwKBgD2PTXSTCKHRqUchiQNwYvt497BBMmGTLpD6DIHF
dBxiHGti5yQPULTeZT3aZmlnYaT+raSWkhvvxqYgm+Lnh3wq7MWnjanaQpEJmujJ
1WpwLrL6NR98IqCpmTvLAsPOiye6+WWuTZi+aKBU5Zy2yQCfgExqw0ax2f3dRD/C
bH1ZAoGAOJ/pLNpetFyE/aaD0jBfMA6UACdutjWT4vFGmk/GwBh3/sHoMbON2c/P
OeEM/N3/ZODOZHzXB1ALgWIjeoP2TegBfbniHf2d+j1/VRMTiYEMv3ws06YiWMLJ
ioX2ZNntCCPlIti48TeFs0etqcHQgQ5rSLblyde3RIuRcqatQko=
-----END RSA PRIVATE KEY-----
'''

# RSA Encrypter using m2crypto
class RSAEncrypterM2:
	def __init__(self):
		from M2Crypto import RSA
		self.cipher = RSA.load_key_string(GWS_KEY)

	def private_encrypt(self, data):
		from M2Crypto import RSA
		return self.cipher.private_encrypt(data, RSA.pkcs1_padding)

# RSA Encrypter using pycrypto
class RSAEncryperCrypto:
	def __init__(self):
		from Crypto.PublicKey import RSA
		self.key = RSA.importKey(GWS_KEY)

	def private_encrypt(self, data):
		pad = "\x01" + "\xFF" * (self.key.size() / 8 - len(data) - 2) + "\x00"
		return self.key.decrypt(pad + data)  # Crypto.RSA "decrypt" is analogous to encrypting with private key

try:
	RSA_ENCRYPTER = RSAEncrypterM2()
except ImportError:
	RSA_ENCRYPTER = RSAEncryperCrypto()  # Fallback

def rsaEncrypt(data):
	return base64.b64encode(RSA_ENCRYPTER.private_encrypt(data))

def random_token():
	chars = string.letters + string.digits
	return ''.join(random.choice(chars) for x in range(48))

def padding(text):
	if isinstance(text, str):
		text = text.encode('utf-8')
	paddingNum = 16 - (len(text) % 16)
	for i in range(paddingNum):
		text += chr(paddingNum)
	return text

def rePadding(text):
	paddingNum = ord(text[len(text) - 1])
	text = text[:(len(text) - paddingNum)]
	return text

EncodeAES = lambda c, s: base64.b64encode(c.encrypt(s))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e))

class Crypt:
	cipher = None
	token = None
	def __init__(self):
		self.token = random_token()
	def getSendData(self, send):
		self.cipher = AES.new(self.token[:32], AES.MODE_CBC, self.token[32:48])
		return EncodeAES(self.cipher, padding(send))
	def getRecvData(self, recv):
		self.cipher = AES.new(self.token[:32], AES.MODE_CBC, self.token[32:48])
		return rePadding(DecodeAES(self.cipher, recv))
	def getRsaToken(self):
		return rsaEncrypt(self.token)

import hashlib
import requests
from xml.dom import minidom
from xml.dom.minidom import Document

AUTH_KEY = '{C390066B-E47B-4476-943B-0B2FBB879660}'

class GWebService:
	crypt = Crypt()

	def __init__(self, module, method, parameters, appid):
		self.module = module
		self.method = method
		self.parameters = parameters
		self.req = self.requestXML(appid, module, method, parameters)

	def reqPlainTextXML(self, appid, moduleName, methodName, params):
		if not isinstance(params, list):
			return None

		doc = Document()

		#<request>
		request = doc.createElement('request')
		doc.appendChild(request)

		#<appid>
		eAppid = doc.createElement('appid')
		request.appendChild(eAppid)
		eAppid.appendChild(doc.createTextNode(appid))

		#<module>
		module = doc.createElement('module')
		request.appendChild(module)
		eModuleName = doc.createElement('name')
		module.appendChild(eModuleName)
		eModuleName.appendChild(doc.createTextNode(moduleName))

		method = doc.createElement('method')
		module.appendChild(method)

		eMethodName = doc.createElement('name')
		method.appendChild(eMethodName)
		eMethodName.appendChild(doc.createTextNode(methodName))

		eParams = doc.createElement('params')
		method.appendChild(eParams)

		sigStr = '' + appid + '|' + moduleName + '|' + methodName + '|' + AUTH_KEY +'|'
		for p in params:
			p = p.lstrip()
			param = doc.createElement('param')
			param.appendChild(doc.createTextNode(p))
			eParams.appendChild(param)
			sigStr += (p + '|')

		sig = doc.createElement('signature')
		request.appendChild(sig)
		sig.appendChild(doc.createTextNode(hashlib.sha1(sigStr.encode('utf-8')).hexdigest()))

		return doc.toxml()

	def requestXML(self, appid, moduleName, methodName, params):
		plainText = self.reqPlainTextXML(appid, moduleName, methodName, params)
		if plainText is None:
			return None
		doc = Document()
		request = doc.createElement('request')
		doc.appendChild(request)

		token = doc.createElement('token')
		request.appendChild(token)
		token.appendChild(doc.createTextNode(self.crypt.getRsaToken()))

		content = doc.createElement('content')
		request.appendChild(content)
		content.appendChild(doc.createTextNode(self.crypt.getSendData(plainText)))

		return doc.toxml()

	def responseXML(self, xml):
		xmldoc = minidom.parseString(xml)
		eContent = xmldoc.getElementsByTagName('content')[0]
		content = self.crypt.getRecvData(eContent.childNodes[0].toxml())
		contentXml = minidom.parseString(content)
		result = contentXml.getElementsByTagName('result')[0].childNodes[0].toxml()

		bodies = []

		try:
			body = contentXml.getElementsByTagName('body')[0].childNodes[0].data
		except:
			return [result, bodies]

		items = body.split('\n')
		col = items[0].split(',')[:-1]

		for item in items[1:-1]:
			ds = item.split(',')[:-1]
			if len(ds) == len(col):
				body = {}
				for i in range(len(ds)):
					body.update({col[i]: ds[i]})
				bodies.append(body)

		return [result, bodies]

	def request(self, address):
		header = {
			'Host': 'www.garena.com',
			'Content-type': 'text/xml;charset=\"utf-8\"'
		}
		r = requests.post("http://%s/index.html" % address, headers=header, data=self.req, timeout=20)
		if r.status_code == 200:
			return self.responseXML(r.content)

from .logger import log

class WebServiceResult:

	GWS_UNKNOWN_ERROR = -1
	GWS_SUCCESS = 0x00000000
	GWS_USER_NOT_EXIST = 0x00000001
	GWS_USER_PWD_NOT_MATCH = 0x00000002
	GWS_USER_EMAIL_NOT_EXIST = 0x00000003
	GWS_USER_EMAIL_NOT_MATCH = 0x00000009
	GWS_USER_EMAIL_UNVERIFY = 0x0000000E
	GWS_TOKEN_NOT_EXIST = 0x00000020
	GWS_OTP_SEED_NOT_EXIST = 0x00000100
	GWS_OTP_TEMPSEED_NOT_EXIST = 0x00000101
	GWS_OTP_TEMPSEED_NOT_ACTIVE = 0x00000102
	GWS_OTP_TEMPSEED_EXPIRE = 0x00000103
	GWS_OTP_TOKEN_NOT_EXIST = 0x00000104
	GWS_OTP_VERIFY_FAILED = 0x00000105
	GWS_OTP_GENERATE_PASSCODE_FAILED = 0x00000106
	GWS_OTP_2STEP_VERIFY_DISABLED = 0x00000107
	GWS_OTP_REVOKE_NOT_ALLOW = 0x00000108
	GWS_OTP_AUTHENTICATOR_DUPLICATE = 0x00000109
	GWS_OTP_EXCEED_SMS_LIMIT = 0x0000010B
	GWS_DB_EXCEPTION = 0x0001003
	GWS_USER_RESERVE_NAME = 0x0000000A
	GWS_SHOP_DEFICIENT_SHELLS = 0x00000050
	GWS_USER_ACNTS_NOT_EXIST = 0x00000007
	GWS_TOPUP_INVALID_SHELLS = 0x00000080
	GWS_TOPUP_INVALID_CARD = 0x00000081
	GWS_TOPUP_USED_CARD = 0x00000082
	GWS_PAYMENT_DEFICIENT_SHELLS = 0x00000091
	GWS_INVALID_INPUT_PARAMS = 0x00001002
	GWS_EXT_FACEBOOK_NOT_EXIST = 0x000000B0
	GWS_CLAN_NOT_EXIST = 0x000000C0
	GWS_CLAN_DUPLICATE_CHALNG = 0x000000C9
	GWS_CLAN_DUPLICATE_MEMBER = 0x000000C7
	GWS_CLAN_DUPLICATE_REQUEST = 0x000000C8
	GWS_CLAN_EVENT_NOT_EXIST = 0x000000C3
	GWS_HON_INFO_NOT_EXIST = 0x000000E0
	GWS_TOPUP_INVALID_CARD_STATE = 0x0000008B
	GWS_TOPUP_EXPIRE_CARD = 0x0000008A
	GWS_DATA_CORRUPT = 0xffffffff

	VALUE_TO_NAME = dict((v, k.lower()) for k, v in list(locals().items()) if not k.startswith('_'))
	NAME_TO_VALUE = dict((value, key) for key, value in list(VALUE_TO_NAME.items()))

class GWebServiceClient():

	def __init__(self, address, app_id):
		self._app_id = app_id
		self._address = address

	def request(self, method, *args):
		sep_index = method.find('.')
		request_args = [str(a) for a in args]
		service = GWebService(method[:sep_index], method[sep_index+1:], request_args, self._app_id)
		response = service.request(self._address)
		result = int(response[0])
		bodies = response[1]
		log.data('gwebservice_request|method=%s,args=%s,result=%d', method, ','.join(request_args), result)
		return result, bodies
