# pylint: disable=ungrouped-imports, wildcard-import
import inspect
import os
import sys	# pylint: disable=unused-import
import copy
import time
import json	# pylint: disable=unused-import
from contextlib import contextmanager
from functools import wraps
from .logger import log
from .convert import *
from . import crypt
import random
import string
import re
import html.parser
import datetime
from .constants import BaseResult

class ClassPropertyMetaClass(type):
	def __setattr__(cls, key, value):
		if key in cls.__dict__:
			obj = cls.__dict__.get(key)
			if obj and isinstance(obj, ClassPropertyDescriptor):
				return obj.__set__(cls, value)
		super(ClassPropertyMetaClass, cls).__setattr__(key, value)

class ClassPropertyDescriptor(object):
	def __init__(self, fget, fset=None):
		self.fget = fget
		self.fset = fset

	def __get__(self, obj, klass=None):
		if klass is None:
			klass = type(obj)
		return self.fget.__get__(obj, klass)()

	def __set__(self, obj, value):
		if not self.fset:
			raise AttributeError("can't set attribute")
		if inspect.isclass(obj):
			type_ = obj
			obj = None
		else:
			type_ = type(obj)
		return self.fset.__get__(obj, type_)(value)

	def setter(self, func):
		if not isinstance(func, (classmethod, staticmethod)):
			func = classmethod(func)
		self.fset = func
		return self

def classproperty(func):
	"""
		-- usage --
		1) simple read:
				...
				@classproperty
				def MY_VALUE(cls):
					return cls._MY_VALUE
				...

		2) simple write: (write by instance)
				...
				// add setter
				@MY_VALUE.setter
				def MY_VALUE(cls, value):
					cls._MY_VALUE = value

		3) complete write: (write by instance or class)
				...
				// add metaclass
				__metaclass__ = ClassPropertyMetaClass

	"""
	if not isinstance(func, (classmethod, staticmethod)):
		func = classmethod(func)
	return ClassPropertyDescriptor(func)

class Object:
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)

def dict_to_object(d):
	return Object(**d)

def create_object(**kwargs):
	return Object(**kwargs)

def find_first(f, seq):
	"""Return first item in sequence where f(item) == True."""
	for item in seq:
		if f(item):
			return item
	return None

def get_timestamp():
	return int(time.time())

def get_timestamp_ms():
	return int(round(time.time() * 1000))

def find_str(text, prefix, suffix=None):
	start = text.find(prefix)
	if start < 0:
		return None
	start += len(prefix)
	if suffix is None:
		return text[start:]
	end = text.find(suffix, start)
	if end < 0:
		return None
	return text[start:end]

def truncate_unicode(text, max_length, encoding='utf-8', ending='...'):
	encoded_str = text.encode(encoding)
	if len(encoded_str) <= max_length:
		return text
	max_length -= len(ending)
	if max_length < 0:
		max_length = 0
	encoded_str = encoded_str[:max_length]
	return encoded_str.decode(encoding, 'ignore') + ending

def exception_safe(exception_return=None, keyword=None, return_filter=copy.copy):
	def _exception_safe(func):
		@wraps(func)
		def _func(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			except:
				if keyword is None:
					log.exception('%s_exception', func.__name__)
				else:
					log.exception('%s_exception', keyword)
				if return_filter:
					return return_filter(exception_return)
				else:
					return exception_return
		return _func
	return _exception_safe

@contextmanager
def directory(path):
	current_dir = os.getcwd()
	os.chdir(path)
	try:
		yield
	finally:
		os.chdir(current_dir)

IS_DJANGO_APP = False
IS_FLASK_APP = False

try:
	from django.conf import settings
	IS_DJANGO_APP = settings.configured
except:
	pass

if not IS_DJANGO_APP:
	try:
		import flask	# pylint: disable=unused-import
		IS_FLASK_APP = True
	except:
		pass

if IS_DJANGO_APP:
	from .django_utils import *
elif IS_FLASK_APP:
	from .flask_utils import *

def with_cache(cache_key_prefix, timeout=60*60):
	def _with_cache(func):
		@wraps(func)
		def _func(key):
			cache_key = cache_key_prefix + crypt.md5(key)
			cache_data = cache.get(cache_key)
			if cache_data is not None:
				if cache_data[0] == key:
					return cache_data[1]
			data = func(key)
			cache_data = (key, data)
			cache.set(cache_key, cache_data, timeout)
			return data
		return _func
	return _with_cache

def ran_gen(size, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

def random_string(seed_str, length=8):
	seed_str = crypt.md5(str(seed_str))
	return ran_gen(length, seed_str)

def get_local_ip():
	import socket
	return socket.gethostbyname(socket.gethostname())

def contains_html(text):
	if not text:
		return False
	return re.search(r'<[^>]*>', text)

def strip_html(text):
	if not text:
		return ''
	parser = html.parser.HTMLParser()
	text = re.sub(r'<[^>]*>', '', text)
	text = parser.unescape(text)
	return text


def date_range(start_date, end_date):
	for n in range(int((end_date - start_date).days)):
		yield start_date + datetime.timedelta(n)

def try_parse_int(data):
	try:
		data = int(data)
		return data
	except Exception as ex:
		return None

def get_distance(src_location, dst_location):
	import math
	dlat = math.radians(dst_location[0] - src_location[0])
	dlon = math.radians(dst_location[1] - src_location[1])
	a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(src_location[0])) * math.cos(math.radians(dst_location[0])) * math.sin(dlon / 2) * math.sin(dlon / 2)
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	d = 6371e3 * c
	return d


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


def convert_client_version(str_version: str):
	if not str_version:
		return 0
	str_version = str_version.replace(".", "")
	ver_length = len(str_version)
	if ver_length > 4:
		return -1
	client_version = int(str_version) * (10 ** (4 - ver_length))
	return client_version


def api_response_data(result_code, reply=None):
	if IS_DJANGO_APP:
		from django import http
		response = http.HttpResponse(jsonutils.to_json({"result": result_code, "reply": reply}))
		response['content-type'] = 'application/json; charset=utf-8'
		response['X_RESULT_CODE'] = result_code
		return response
	else:
		return api_response({"result": result_code, "reply": reply})


def api_response_error_params(*args):
	return api_response_data(BaseResult.ERROR_PARAMS)


def api_response_error_defined_message(error_message=None, error_localize_message=None, error_title=None, error_localize_title=None):
	if error_message:
		response_message = format_localization(message=error_message)
	else:
		response_message = error_localize_message
	if error_title:
		response_title = format_localization(message=error_title)
	else:
		if error_localize_title is None:
			response_title = format_localization(resource_name='title_api_error')
		else:
			response_title = error_localize_title
	return api_response_data(BaseResult.ERROR_DEFINED_MESSAGE, {'title': response_title, 'message': response_message})


def format_localization(message=None, resource_name=None, resource_args=None):  # resource_args must array string
	result = {}
	if message:
		result['message'] = message
	if resource_name:
		result['resource_name'] = resource_name
		if resource_args:
			result['resource_args'] = resource_args
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

