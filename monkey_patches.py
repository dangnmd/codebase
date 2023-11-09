def _monkey_patch():
	import platform
	if platform.system().lower() == 'windows':
		return

	import inspect
	import os
	import socket
	import sys
	import time
	import uuid
	import baseconv
	from functools import wraps

	from gevent import GreenletExit
	from gevent import _socket2
	from gevent import _socketcommon
	from gevent import monkey
	from gevent import threading
	from gunicorn.workers import ggevent


	class PatchedStreamServer(ggevent.StreamServer):
		def __init__(self, listener, spawn=None, **kwargs):
			super(PatchedStreamServer, self).__init__(listener, spawn=spawn, **kwargs)
			caller = inspect.currentframe().f_back.f_locals['self']
			if hasattr(spawn, 'spawn'):
				spawn.spawn(self.log_greenlet_count, caller.age, spawn)

		@staticmethod
		def log_greenlet_count(worker_id, pool):
			# from common.logger import log
			# pid = os.getpid()

			from prometheus_client import Gauge
			available_greenlets = Gauge('available_greenlets', 'Available greenlets', [])

			while True:
				# log.info('greenlet_count|workerid=%s,pid=%s,used=%s,free=%s', worker_id, pid, len(pool),
				# 	free_count)

				free_count = pool.free_count()
				available_greenlets.set(free_count)

				start_time = time.time()
				offset = start_time - int(start_time)
				if offset > 0:
					ggevent.gevent.sleep(1 - offset)


	ggevent.StreamServer = PatchedStreamServer


	def catch_greenletexit(func):
		@wraps(func)
		def _catch_greenletexit(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			except GreenletExit:
				from common.logger import log
				log.exception('first_catch_greenletexit|%s', locals())
				ex_type, ex_value, ex_traceback = sys.exc_info()
				raise socket.timeout(ex_value).with_traceback(ex_traceback)

		return _catch_greenletexit


	_socket2.socket.send = catch_greenletexit(_socket2.socket.send)
	_socket2.socket.recv_into = catch_greenletexit(_socket2.socket.recv_into)
	_socket2.socket.recv = catch_greenletexit(_socket2.socket.recv)
	_socket2.socket.connect = catch_greenletexit(_socket2.socket.connect)

	monkey.patch_all()

	socket.getaddrinfo = catch_greenletexit(socket.getaddrinfo)

	# Patch gunicorn's logger to use common logger to print log.
	# Otherwise, when process request failed, it would not print exceptions.
	from gunicorn.workers.base import Worker
	worker_init = Worker.__init__

	def patched_worker_init(self, age, ppid, sockets, app, timeout, cfg, log):
		worker_init(self, age, ppid, sockets, app, timeout, cfg, log)
		from common.logger import log
		self.log.critical = self.log.critical
		self.log.error = log.error
		self.log.warning = log.warning
		self.log.info = log.info
		self.log.debug = log.debug
		self.log.exception = log.exception
		self.log.log = log.log

	Worker.__init__ = patched_worker_init

	# Closed unnecessary MySQL connections.
	import gunicorn.util as util
	def close(sock):
		from django.db import connections
		for conn in connections.all():
			try:
				conn.abort()
			except:
				pass
			conn.close()
		try:
			sock.close()
		except socket.error:
			pass
	util.close = close

_monkey_patch()