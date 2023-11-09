# pylint: disable=unexpected-keyword-arg, unnecessary-lambda
# Credit to Nicholas Kwan
import glob
import os
import re
import time

import psutil
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.http.response import HttpResponseForbidden
from prometheus_client import CONTENT_TYPE_LATEST
from prometheus_client import Summary, Counter, Gauge
from django.utils.deprecation import MiddlewareMixin
from config import config
from common.utils import get_request_ip

IP_LIST = []


def white_list_ip(addr):
	"""
	Function to help whitelist ip. If ip is not in the file ip-whitelist.txt, then return false. Supports basic
	wildcard matching
	:param addr:
	:return:
	"""
	global IP_LIST
	if not IP_LIST:
		for ip in config.METRICS_IP_WHITELIST:
			# process addr to become regex pattern
			address = ip  # .replace('.', "\\.").replace('*', '[0-9]{3}')
			IP_LIST.append(address)

	for ip in IP_LIST:
		if re.search(ip, addr):
			return True
	return False


def cleanup_old_files(init=False):
	# Clear unnecessary prometheus db files.
	now = int(time.time())
	for f in glob.glob(os.path.join(os.environ.get('prometheus_multiproc_dir'), '*.db')):
		parts = os.path.basename(f).replace(".db", "").split('_')
		try:
			pid = int(parts[-1])
			if not psutil.pid_exists(pid) and ((now - int(os.path.getmtime(f))) > 60 or init):
				os.remove(f)
		except (ValueError, OSError):
			continue


# Shared logic between Django web and logic server
class MetricsManager(object):
	COLLECTORS = {}
	PROCESS_OBSERVE_INTERVAL = 1  # In seconds
	PROCESS_LAST_OBSERVE_TIME = 0

	# Init all the metrics
	@classmethod
	def init_class(cls):
		# prometheus_client should not be initialized at pre-fork (point at which this module is loaded)
		# otherwise multiple children may attempt to write to same MMap file in Prometheus
		# Instead, we initialize it when we are about to record something
		if cls.COLLECTORS:
			return

		cls.COLLECTORS = {
			"requests_total": Counter('requests_total', 'Number of requests', ['status_code', 'endpoint', 'result_code']),
			"request_latency": Summary('request_latency_seconds', 'Request latency', ['status_code', 'endpoint']),
			"request_size": Summary('request_size_bytes', 'Request size', ['status_code', 'endpoint']),
			"response_size": Summary('response_size_bytes', 'Response size', ['status_code', 'endpoint']),
			"worker_virtual_memory": Gauge('worker_virtual_memory', 'Virtual Memory', ['pid'],
										   multiprocess_mode='livesum'),
			"worker_resident_memory": Gauge('worker_resident_memory', 'Resident Memory', ['pid'],
											multiprocess_mode='livesum'),
			"worker_cpu_time": Gauge('worker_cpu_time', 'CPU Time', ['pid'], multiprocess_mode='livesum'),
			"worker_fds": Gauge('worker_fds', 'File Descriptor', ['pid'], multiprocess_mode='livesum'),
		}

	@classmethod
	def observe_process(cls):
		try:
			now = int(time.time())
			if now - cls.PROCESS_LAST_OBSERVE_TIME < cls.PROCESS_OBSERVE_INTERVAL:
				return  # Don't need to record observation on every request to reduce sample count
			cls.PROCESS_LAST_OBSERVE_TIME = now

			pid = os.getpid()
			p = psutil.Process(pid)
			cpu_time = p.cpu_times()
			vmem = p.memory_info()

			cls.COLLECTORS["worker_virtual_memory"].labels(pid=pid).set(vmem.vms)
			cls.COLLECTORS["worker_resident_memory"].labels(pid=pid).set(vmem.rss)
			cls.COLLECTORS["worker_cpu_time"].labels(pid=pid).set(cpu_time.user + cpu_time.system)
			if os.name != "nt":
				cls.COLLECTORS["worker_fds"].labels(pid=pid).set(p.num_fds())
		except:
			pass

	# Django web: status_code = HTTP status code, result_code = Result, endpoint = URL
	# Logic server: status_code = Result, result_code = Result, endpoint = Command
	@classmethod
	def observe_request(cls, status_code, result_code, endpoint, elapsed, req_length=0, res_length=0):
		cls.init_class()
		cls.COLLECTORS["requests_total"].labels(status_code=status_code, endpoint=endpoint, result_code=result_code).inc()
		cls.COLLECTORS["request_latency"].labels(status_code=status_code, endpoint=endpoint).observe(elapsed)
		if req_length:
			cls.COLLECTORS["request_size"].labels(status_code=status_code, endpoint=endpoint).observe(int(req_length))
		if res_length:
			cls.COLLECTORS["response_size"].labels(status_code=status_code, endpoint=endpoint).observe(int(res_length))
		cls.observe_process()

	@classmethod
	def purge_data(cls):
		if 'prometheus_multiproc_dir' not in os.environ:
			return

		# Purge metrics mmap files when data corrupt.
		# Refer https://github.com/prometheus/client_python/issues/127 for details.
		for f in glob.glob(os.path.join(os.environ.get('prometheus_multiproc_dir'), '*.db')):
			try:
				os.remove(f)
			except:
				pass

		cls.recreate_db()

	@classmethod
	def recreate_db_file(cls, mm_map, mm_value):
		mm_file_obj = getattr(mm_value, "_file")
		file_name = getattr(mm_file_obj, "_f").name
		prefix = "_".join(os.path.basename(file_name).split("_")[:-1])

		if prefix not in mm_map:
			if os.path.exists(file_name):
				return  # File present, no need to recreate

			import prometheus_client
			mm_map[prefix] = getattr(prometheus_client.core, "_MmapedDict")(file_name)
		setattr(mm_value, "_file", mm_map[prefix])  # Some metrics write > 1 value to same file, so need to reuse it

	@classmethod
	def recreate_db_for_collector(cls, mm_map, collector):
		if hasattr(collector, "_metrics"):
			# Handle wrapped metric classes
			metric_map = getattr(collector, "_metrics")
			for metric_key in metric_map:
				cls.recreate_db_for_collector(mm_map, metric_map[metric_key])
			return
		# These are possible attributes which has _ValueClass
		for attribute in ["_value", "_count", "_sum"]:
			if not hasattr(collector, attribute):
				continue
			mm_value = getattr(collector, attribute)
			cls.recreate_db_file(mm_map, mm_value)
		# Handle histogram
		if hasattr(collector, "_buckets"):
			buckets = getattr(collector, "_buckets")
			for bucket in buckets:
				cls.recreate_db_file(mm_map, bucket)

	# Recreate the files if they are missing so tracking will resume correctly
	@classmethod
	def recreate_db(cls):
		mm_map = {}  # This dictionary is for tracking _ValueClass, needed for Metrics that use > 1 _ValueClass
		for collector_key in cls.COLLECTORS:
			cls.recreate_db_for_collector(mm_map, cls.COLLECTORS[collector_key])

	@classmethod
	def do_snapshot(cls):
		from prometheus_client import CollectorRegistry, generate_latest
		from prometheus_client.multiprocess import MultiProcessCollector
		data = ""
		try:
			registry = CollectorRegistry()
			MultiProcessCollector(registry)
			data = generate_latest(registry)
			cls.recreate_db()
		except:
			cls.purge_data()
		return data


# Modified from common.django_utils.MetricsMiddleware
class ExtendedMetricsMiddleware(MiddlewareMixin):
	def process_request(self, request):
		request.metrics_start_time = time.time()

	def process_response(self, request, response):
		if not response.status_code:
			return response

		if request.resolver_match is None:
			return response

		elapsed = time.time() - request.metrics_start_time
		status_code = response.status_code
		result_code = response.get("X_FOODY_RESULT_CODE", status_code)
		url_rule = request.META.get("PATH_INFO", "/")

		try:
			req_length = request.META.get('CONTENT_LENGTH')
			res_length = len(response.content) if response.content else 0
			MetricsManager.observe_request(status_code, result_code, url_rule, elapsed, req_length, res_length)
		except Exception as e:
			import traceback
			print((traceback.print_exc()))
			MetricsManager.purge_data()

		return response

	@classmethod
	def metrics_snapshot(cls, request):
		# if ip address is not whitelisted, return response forbidden
		ip_address = get_request_ip(request)
		if ip_address and not white_list_ip(ip_address):
			return HttpResponseForbidden()
		return HttpResponse(MetricsManager.do_snapshot(), content_type=CONTENT_TYPE_LATEST)


# For logic server processor
class ProcessorMetricsMiddleware(object):
	@classmethod
	def process_response(cls, result_code, cmd, elapsed, request_str, reply_str):
		try:
			req_length = len(request_str) if request_str else 0
			res_length = len(reply_str) if reply_str else 0
			MetricsManager.observe_request(result_code, result_code, "%s" % cmd, elapsed, req_length, res_length)
		except:
			MetricsManager.purge_data()

	@classmethod
	def metrics_snapshot(cls):
		return MetricsManager.do_snapshot()
