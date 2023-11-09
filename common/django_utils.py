import sys
import time
from functools import wraps
from lxml import etree
from django import http
from django.views import defaults
from django.core.signals import request_finished
from django.template.defaultfilters import register
from django.utils.safestring import mark_safe
from jsonschema import Draft4Validator
from . import jsonutils
from .logger import log
from .useragent import UserAgent
from .form_validator import FormValidator
from . import convert

def response_http_400(request):
	return defaults.bad_request(request)

def response_http_404(request):
	return defaults.page_not_found(request)

def response_http_500(request):
	return defaults.server_error(request)

def response_redirect(request, uri):
	response = http.HttpResponse()
	response.status_code = 302
	response['Location'] = uri
	return response

def api_xml_response(request, data, xml_declaration=True, encoding='utf-8'):
	response = http.HttpResponse(etree.tostring(data, pretty_print=True, xml_declaration=xml_declaration, encoding=encoding))
	return response

def api_response(request, data):
	response = http.HttpResponse(jsonutils.to_json(data), content_type='application/json; charset=utf-8')
	return response


def ensure_str(potential_bytes, minify=False):
	if isinstance(potential_bytes, bytes):
		value = potential_bytes.decode('utf-8')
	else:
		value = potential_bytes
	if minify:
		return minify_str(value)
	return value  # Instance of str


def minify_str(input_str):
	input_str_split = input_str.split()
	return "".join(input_str_split)

def get_request_ip(request):
	if not getattr(request, 'META'):
		return ''
	ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
	# Note: HTTP_X_FORWARDED_FOR might be a list of addresses!
	# NOTE: We only trust the LAST address because it's the proxy address. All IPs before the last one can be mocked by sender.
	if ',' in ip:
		ip = [x for x in [x.strip() for x in ip.split(',')] if x][-1]
	return ensure_str(ip)

def ip_restrict(allow_list, error_handler=response_http_404):
	def _ip_restrict(func):
		@wraps(func)
		def _func(request, *args, **kwargs):
			ip = get_request_ip(request)
			if ip not in allow_list:
				log.warning('unauthorized_ip|ip=%s', ip)
				return error_handler(request)
			return func(request, *args, **kwargs)
		return _func
	return _ip_restrict

def parse_params(form, method='GET', data_format='FORM', error_handler=response_http_404, parse_ua=False, check_method=True, encoding=None):
	if isinstance(form, dict):
		if data_format == 'FORM':
			form = FormValidator(form)
		elif data_format == 'JSON':
			form = Draft4Validator(form)
	def _parse_params(func):
		func.schema = form
		func.method = method
		@wraps(func)
		def _func(request, *args, **kwargs):
			if check_method and request.method != method:
				log.warning('view_method_error|url=%s,method=%s', request.get_full_path(), request.method)
				return error_handler(request)
			if encoding:
				request.encoding = encoding
			if data_format == 'XML':
				try:
					xml_data = etree.XML(request.body)
				except:
					log.warning('view_params_error|format=xml,url=%s,body=%s', request.get_full_path(), request.body)
					return error_handler(request)
				if not form(xml_data):
					log.warning('view_params_schema_error|format=xml,url=%s,error=%s,body=%s', request.get_full_path(), form.error_log, request.body)
					return error_handler(request)
				data = {'xml_data': xml_data}
			else:
				if isinstance(form, (FormValidator, Draft4Validator)):
					if method == 'GET':
						formdata = request.GET
					elif data_format == 'JSON':
						formdata = {}
						if request.body:
							try:
								formdata = jsonutils.from_json(request.body)
							except Exception as err:
								log.warning('view_params_error|format=json,url=%s,body=%s,err=%s', request.get_full_path(), request.body,err)
								#return error_handler(request)
								formdata = {}
					else:
						formdata = request.POST
					try:
						if isinstance(form, FormValidator):
							data = form.normalize(formdata)
						else:
							form.validate(formdata)
							data = formdata
					except Exception as ex:
						log.warning('view_params_error|format=form,url=%s,error=%s,body=%s', request.get_full_path(), ex, formdata)
						return error_handler(request)
				else:
					if method == 'GET':
						dataform = form(request.GET)
					elif data_format == 'JSON':
						try:
							dataform = form(jsonutils.from_json(request.body))
						except:
							log.warning('view_params_error|format=json,url=%s,body=%s', request.get_full_path(), request.body)
							return error_handler(request)
					elif data_format == 'MULTIPART':
						dataform = form(request.POST, request.FILES)
					else:
						dataform = form(request.POST)

					if not dataform.is_valid():
						if hasattr(request, '_body'):
							request_body = request.body
						else:
							request_body = '<unreadable>'
						log.warning('view_params_error|format=form,url=%s,error=%s,body=%s', request.get_full_path(), dataform.errors.__repr__(), request_body)
						return error_handler(request)
					data = dataform.cleaned_data
			data['_request_ip'] = get_request_ip(request)
			if parse_ua:
				data['request_ua'] = UserAgent(request.META.get('HTTP_USER_AGENT', ''))
			return func(request, data, *args, **kwargs)
		return _func
	return _parse_params

def log_request(log_response=True, max_response_length=500, log_request_body=True, max_request_body_length=None, header_prefix=None):
	def _log_request(func):
		@wraps(func)
		def _func(request, *args, **kwargs):
			start = time.time()
			global request_exception
			request_exception = None
			response = None
			ex_type = None
			ex_value = None
			ex_traceback = None
			try:
				response = func(request, *args, **kwargs)
			except Exception as _request_exception:
				request_exception = _request_exception
				ex_type, ex_value, ex_traceback = sys.exc_info()
				log.exception('%s_exception', func.__name__)
			end = time.time()
			elapsed = int((end - start) * 1000)
			if log_request_body:
				if hasattr(request, '_body'):
					request_body = ensure_str(request.body, minify=True)
				elif request.POST:
					request_body = 'POST:' + jsonutils.to_json(request.POST, ensure_bytes=False)
					if request.FILES:
						files_info = dict([(k, {v.name: v.size}) for k, v in request.FILES.items()])
						request_body += ';FILES:' + jsonutils.to_json(files_info, ensure_bytes=False)
				else:
					request_body = ''
				if max_request_body_length and len(request_body) > max_request_body_length:
					request_body = request_body[:max_request_body_length] + '...'
			else:
				request_body = ''
			if request_exception is None:
				status_code = response.status_code
				if log_response:
					if (status_code == 301 or status_code == 302) and 'Location' in response:
						response_body = ensure_str(response['Location'])
					else:
						response_body = ensure_str(response.content)
						if max_response_length and len(response_body) > max_response_length:
							response_body = ensure_str(response_body[:max_response_length]) + '...'
				else:
					response_body = ''
			else:
				if request_exception is http.Http404:
					status_code = 404
				else:
					status_code = 500
				response_body = 'exception:%s' % ensure_str(request_exception)
			if header_prefix:
				header_body = {}
				for header_key, header_value in request.META.items():
					if header_key.startswith(header_prefix):
						header_body[header_key.lower()] = header_value
				header_body_str = jsonutils.to_json(header_body)
				log.data('http_request|ip=%s,elapsed=%d,method=%s,url=%s,body=%s,status_code=%d,response=%s,header_body=%s',
					get_request_ip(request), elapsed, request.method, request.get_full_path(), request_body, status_code, response_body, header_body_str)
			else:
				log.data('http_request|ip=%s,elapsed=%d,method=%s,url=%s,body=%s,status_code=%d,response=%s',
					get_request_ip(request), elapsed, request.method, request.get_full_path(), request_body, status_code, response_body)
			if request_exception is not None:
				raise ex_type(ex_value).with_traceback(ex_traceback)
			return response
		return _func
	return _log_request

def geo_ip_to_country(ip):
	try:
		from django.contrib.gis.geoip import GeoIP
		if isinstance(ip, int):
			return GeoIP().country(convert.int_to_ip(ip))['country_code'] or 'ZZ'
		else:
			return GeoIP().country(ip)['country_code'] or 'ZZ'
	except:
		log.exception('geo_ip_to_country_exception')
		return 'ZZ'

_function_queue = []

def _run_all(sender, **kwargs):
	for func, args, kwargs in _function_queue:
		func(*args, **kwargs)
	_function_queue[:] = []

def init_after_response():
	request_finished.connect(_run_all)

def add_after_response(func, *args, **kwargs):
	_function_queue.append((func, args, kwargs))

@register.filter
def tojson(v):
	return mark_safe(jsonutils.to_json_html_safe(v))

class ProxyFixMiddleware(object):
	def process_request(self, request):
		meta = request.META
		forwarded_proto = meta.get('HTTP_X_FORWARDED_PROTO', '')
		forwarded_for = meta.get('HTTP_X_FORWARDED_FOR', '').split(',')
		forwarded_host = meta.get('HTTP_X_FORWARDED_HOST', '')
		forwarded_for = [x for x in [x.strip() for x in forwarded_for] if x]
		remote_addr = None
		if forwarded_for:
			remote_addr = forwarded_for[-1]
		if remote_addr is not None:
			meta['REMOTE_ADDR'] = remote_addr
		if forwarded_host:
			meta['HTTP_HOST'] = forwarded_host
		if forwarded_proto:
			meta['wsgi.url_scheme'] = forwarded_proto


class MetricsMiddleware(object):
	'''
	To use metrics collector based on prometheus, we need to do following steps:

	1. Add this middlware in settings.py
	```
	# In settings.py
	MIDDLEWARE_CLASSES = (
		'common.django_utils.MetricsMiddleware',
		...
	)
	```

	2. Expose metrics information via `/metrics` endpoint.

	```
	from common import django_utils

	urlpatterns = [
		...
		url(r'metrics$', django_utils.MetricsMiddleware.metrics_snapshot),
		...
	]
	```

	3. Set `prometheus_multiproc_dir` to the path of the folder which save prometheus db files.
	'''
	# pylint: disable=protected-access

	_inited = False

	def __init__(self):
		# `prometheus_client` should not be initialized at
		# pre-fork (point at which this module is loaded),
		# otherwise multiple children may attempt to write to same MMap file in Prometheus.
		# Instead, we initialize it when we are about to record something.
		if not MetricsMiddleware._inited:
			MetricsMiddleware._inited = True
			from prometheus_client import Summary, Counter
			MetricsMiddleware.requests_total = Counter('requests_total', 'Number of requests', ['status_code', 'endpoint'])
			MetricsMiddleware.request_latency = Summary('request_latency_seconds', 'Request latency', ['status_code', 'endpoint'])
			MetricsMiddleware.request_size = Summary('request_size_bytes', 'Request size', ['status_code', 'endpoint'])
			MetricsMiddleware.response_size = Summary('response_size_bytes', 'Response size', ['status_code', 'endpoint'])

		# Patch ResolverMatch for metrics.
		from django.core.urlresolvers import ResolverMatch, Resolver404, RegexURLResolver

		def patched_resolve(self, path):
			tried = []
			match = self.regex.search(path)
			if match:
				new_path = path[match.end():]
				for pattern in self.url_patterns:
					try:
						sub_match = pattern.resolve(new_path)
					except Resolver404 as e:
						sub_tried = e.args[0].get('tried')
						if sub_tried is not None:
							tried.extend([[pattern] + t for t in sub_tried])
						else:
							tried.append([pattern])
					else:
						if sub_match:
							sub_match_dict = dict(match.groupdict(), **self.default_kwargs)
							sub_match_dict.update(sub_match.kwargs)
							resolver_match = ResolverMatch(
								sub_match.func,
								sub_match.args,
								sub_match_dict,
								sub_match.url_name,
								self.app_name or sub_match.app_name,
								[self.namespace] + sub_match.namespaces)
							resolver_match.url_regex = pattern.regex.pattern
							if hasattr(sub_match, 'url_regex'):
								resolver_match.url_regex += sub_match.url_regex
							return resolver_match
						tried.append([pattern])
				raise Resolver404({'tried': tried, 'path': new_path})
			raise Resolver404({'path': path})

		RegexURLResolver.resolve = patched_resolve

	def process_request(self, request):
		request._metrics_start_time = time.time()

	def process_response(self, request, response):
		import glob
		import os

		if not response.status_code:
			return response

		if request.resolver_match is None:
			return response

		elapsed = time.time() - request._metrics_start_time
		status_code = response.status_code
		url_rule = request.resolver_match.url_regex[:40]

		try:
			self.requests_total.labels(status_code=status_code, endpoint=url_rule).inc()
			self.request_latency.labels(status_code=status_code, endpoint=url_rule).observe(elapsed)
			if request.META.get('CONTENT_LENGTH'):
				self.request_size.labels(
					status_code=status_code,
					endpoint=url_rule).observe(int(request.META.get('CONTENT_LENGTH')))
			if 'content' in response:
				self.response_size.labels(
					status_code=status_code,
					endpoint=url_rule).observe(len(response.content))
			elif 'streaming_content' in response:
				self.response_size.labels(
					status_code=status_code,
					endpoint=url_rule).observe(len(response.streaming_content))
		except:
			# Purge metrics mmap files when data corrupt.
			# Refer https://github.com/prometheus/client_python/issues/127 for details.
			for f in glob.glob(os.path.join(os.environ.get('prometheus_multiproc_dir'), '*.d')):
				try:
					os.remove(f)
				except:
					pass

		return response

	@staticmethod
	def metrics_snapshot(request):
		import glob
		import os
		from django.http import HttpResponse, HttpResponseNotFound
		from prometheus_client import multiprocess
		from prometheus_client import generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST

		ip = get_request_ip(request)
		if not ip == '' and \
			not ip.startswith('10.') and \
			not ip.startswith('172.') and \
			not ip.startswith('192.168.') and \
			not ip.startswith('127.'):
			return HttpResponseNotFound()

		registry = CollectorRegistry()
		multiprocess.MultiProcessCollector(registry)
		data = generate_latest(registry)

		# Clear unnecessary prometheus db files.
		import psutil
		now = int(time.time())
		for f in glob.glob(os.path.join(os.environ.get('prometheus_multiproc_dir'), '*.d')):
			parts = os.path.basename(f).split('_')
			if len(parts) == 2:
				pid, _unused = parts[1].split('.')
				pid = int(pid)
				try:
					if not psutil.pid_exists(pid) and (now - int(os.path.getmtime(f))) > 60:
						os.remove(f)
				except:
					pass

		return HttpResponse(data, content_type=CONTENT_TYPE_LATEST)
