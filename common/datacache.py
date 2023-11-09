import time


class DataCache(object):
	"""
	In-memory cache wrapper for a value returned by a function.
	To use the class, either subclass this and override `_load_data`
	or pass the load function via `load_data_func` when creating object.
	"""

	TIMEOUT = 60  # timeout seconds

	def __init__(self, timeout=None, load_data_func=None):
		self._cache = None
		self._last_time = 0
		if timeout is None:
			self._timeout = self.TIMEOUT
		else:
			self._timeout = timeout
		self._load_data_func = load_data_func

	def get_data(self):
		curr_time = time.time()
		if self._cache is None or self._last_time + self._timeout < curr_time:
			self._cache = self._load_data()
			self._last_time = curr_time
		return self._cache

	def clear_cache(self):
		self._cache = None

	def _load_data(self):
		"""
		:return: data queried from underlying storage.
		"""
		return self._load_data_func()


class DataCacheTable(object):
	"""
	In-memory cache wrapper for a value returned by a function (that takes in an argument).
	To use the class, either subclass this and override `_load_data`
	or pass the load function via `load_data_func` when creating object.
	"""

	TIMEOUT = 60  #timeout seconds

	def __init__(self, timeout=None, load_data_func=None):
		self._cache = {}
		if timeout is None:
			self._timeout = self.TIMEOUT
		else:
			self._timeout = timeout
		self._load_data_func = load_data_func

	def get_data(self, key):
		curr_time = int(time.time())
		data = self._cache.get(key, None)
		if data is None or data[0] + self._timeout < curr_time:
			cache_data = self._load_data(key)
			data = (curr_time, cache_data)
			self._cache[key] = data
		return data[1]

	def clear_cache(self):
		self._cache = {}

	def _load_data(self, key):
		"""
		:param key: the key of data, can be tuple.
		:return: data queried from underlying storage.
		"""
		return self._load_data_func(key)
