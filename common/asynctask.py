from threading import Thread
import queue
from .logger import log

class _Context:
	runner_thread = None
	task_queue = None

def _run_async_task():
	while True:
		target, args, kwargs = _Context.task_queue.get()
		try:
			target(*args, **kwargs)
		except:
			log.exception('run_async_task_exception|target=%s,args=%s,kwargs=%s', target.__name__, repr(args), repr(kwargs))

def run(target, args=(), kwargs=None):
	if kwargs is None:
		kwargs = {}
	if _Context.task_queue is None:
		_Context.task_queue = queue.Queue()
		_Context.runner_thread = Thread(target=_run_async_task)
		_Context.runner_thread.start()
	_Context.task_queue.put((target, args, kwargs))
