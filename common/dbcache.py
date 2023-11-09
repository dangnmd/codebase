import time
from . import model_utils

class DBCache(object):
	# pylint: disable=protected-access

	TABLE = None	#model
	TIMEOUT = 60	#timeout seconds

	def __init__(self):
		self._cache = None
		self._last_time = 0

	def _get_cache(self):
		curr_time = time.time()
		if self._cache is None or self._last_time + self.TIMEOUT < curr_time:
			self._cache = self.TABLE.objects.all()
			self._last_time = curr_time

	def clear_cache(self):
		self._cache = None

	def _get_data(self, condition):
		self._get_cache()
		return [model_utils.copy_model_object(d) for d in self._cache if condition(d)]

	@staticmethod
	def generate_get_method(condition):
		def _func(self, *args):
			self._get_cache()
			return [model_utils.copy_model_object(d) for d in self._cache if condition(args, d)]
		return _func

	@staticmethod
	def generate_get_one_method(condition):
		def _func(self, *args):
			self._get_cache()
			for data in self._cache:
				if condition(args, data):
					return model_utils.copy_model_object(data)
			return None
		return _func
