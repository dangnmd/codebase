from functools import wraps
import os
import time
import sys
import socket
import select
import ssl
import subprocess
import _thread
import threading
import _threading_local
import importlib


class GeventContext(object):
	"""
	1. THIS IS NOT THREAD SAFE! ie. monkey patches in one thread affect other threads
	2. reload takes 1~10ms, so try not to put the monkey_context in a large loop
	"""
	def __enter__(self):
		from gevent import monkey
		monkey.patch_os()
		monkey.patch_time()
		monkey.patch_thread()
		monkey.patch_sys()
		monkey.patch_socket()
		monkey.patch_select()
		monkey.patch_ssl()
		monkey.patch_subprocess()

	def __exit__(self, exc_type, exc_value, traceback):
		importlib.reload(os)
		importlib.reload(time)
		importlib.reload(thread)
		importlib.reload(threading)
		importlib.reload(_threading_local)
		importlib.reload(sys)
		importlib.reload(socket)
		importlib.reload(select)
		importlib.reload(ssl)
		importlib.reload(subprocess)

	def __call__(self, func):
		@wraps(func)
		def inner(*args, **kwargs):
			with self:
				return func(*args, **kwargs)
		return inner


def gevent_context(func=None):
	"""
	usage:
	1)
	@gevent_context
	def func():
		pass
	2)
	with gevent_context():
		pass
	"""
	if callable(func):
		return GeventContext()(func)
	else:
		return GeventContext()
