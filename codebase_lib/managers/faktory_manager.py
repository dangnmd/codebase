from common import faktory
from common.faktory import worker
from common.faktory._proto import *
from common import logger
from codebase_lib import config
from common.logger import log
import uuid

def add_single_job(job_name, args, **queue_config):
	add_multiple_jobs(job_name, [args], **queue_config)

def add_multiple_jobs(job_name, list_args, **queue_config):
	client_config = {
		'faktory': queue_config['faktory'],
		'log': logger.log
	}
	added_queue = queue_config['queues'][0]
	connection = Connection(**client_config)
	with faktory.connection(connection=connection) as faktory_client:
		for args in list_args:
			faktory_client.queue(job_name, args=args, queue=added_queue)

def get_faktory_config(job_name):
	faktory_config = config.FAKTORY_WORKER_CONFIG["default"]
	if job_name in config.FAKTORY_WORKER_CONFIG:
		faktory_config = config.FAKTORY_WORKER_CONFIG[job_name]
	faktory_config['log'] = log
	return faktory_config

def create_worker(job_name, job_fn):
	worker_config = get_faktory_config(job_name)
	worker_config['worker_id'] = '%s-%s' % (uuid.uuid4().hex, job_name)
	faktory_worker = worker.Worker(**worker_config)
	faktory_worker.register(job_name, job_fn)
	return faktory_worker

def start_worker(job_name, job_fn):
	try:
		create_worker(job_name, job_fn).run()
	except Exception as ex:
		log.error("start_worker_error|ex=%s", ex)


class FaktoryClient(object):
	def __init__(self, job_type, worker_fn=None):
		self._job_type = job_type
		self._config = get_faktory_config(job_type)
		self._job_fn = worker_fn

	def add_queues(self, list_args):
		add_multiple_jobs(self._job_type, list_args, **self._config)

	def process(self):
		start_worker(self._job_type, self._job_fn)
