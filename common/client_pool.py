"""
This module provide common thread / coroutine safe client managers for any client.
"""

from collections import deque
import threading
from contextlib import contextmanager

class ClientPool(object):
	"""
	ClientPool maintains clients pool with max size or unlimited size, and it ensures thread / coroutine safe,
	new client will be created on demand.

	Usage:

	pool = ClientPool(GTcpClient, ('localhost', 80), 8)

	# use `with` statement
	with pool.get() as client:
		reply = client.request('test')

	# or manually `fetch` and `put`
	try:
		client = pool.fetch()
		reply = client.request('test')
	finally:
		pool.put(client)

	# call `discard` if the client encountered error and can not be used any more.
	pool.discard(client)
	"""

	def __init__(self, initializer, init_args=(), init_kwargs=None, size=None):
		if init_kwargs is None:
			init_kwargs = {}
		self._initializer = initializer
		self._init_args = init_args
		self._init_kwargs = init_kwargs
		self._size = size
		if self._size is not None and self._size <= 0:
			self._size = None
		self._clients = set()
		self._queue = deque()
		self._lock = threading.Lock()
		self._not_empty_cv = threading.Condition(self._lock)

	@contextmanager
	def get(self):
		client = self.fetch()
		try:
			yield client
		finally:
			self.put(client)

	def fetch(self):
		self._lock.acquire()
		while len(self._queue) <= 0:
			if self._size is None or len(self._clients) < self._size:
				self._lock.release()
				client = self._initializer(*self._init_args, **self._init_kwargs)
				self._lock.acquire()
				if self._size is None or len(self._clients) < self._size:
					self._clients.add(client)
					self._lock.release()
					return client
			else:
				self._not_empty_cv.wait()
		client = self._queue.popleft()
		self._lock.release()
		return client

	def put(self, client):
		self._lock.acquire()
		if client in self._clients:
			self._queue.append(client)
			if len(self._queue) <= 1:
				self._not_empty_cv.notify_all()
		self._lock.release()

	def discard(self, client):
		self._lock.acquire()
		self._clients.discard(client)
		self._not_empty_cv.notify_all()
		self._lock.release()

class ThreadLocalClient(object):
	"""
	ThreadLocalClient maintains thread / coroutine local client,
	it will maintains one client for each thread / coroutine.

	Usage:

	client = ThreadLocalClient(GTcpClient, ('localhost', 80), 8)

	# use client
	client.get().request('test')

	# call `reset` if the client encountered error and can not be used any more.
	client.reset()
	"""

	def __init__(self, initializer, init_args=(), init_kwargs=None):
		if init_kwargs is None:
			init_kwargs = {}
		self._initializer = initializer
		self._init_args = init_args
		self._init_kwargs = init_kwargs
		self._client = threading.local()

	def get(self):
		client = getattr(self._client, 'client', None)
		if client is None:
			client = self._initializer(*self._init_args, **self._init_kwargs)
			self._client.client = client
		return client

	def set(self, client):
		self._client.client = client

	def reset(self):
		self._client.client = None
