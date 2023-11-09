from collections import deque

class SimpleQueue():

	def __init__(self, max_size=None):
		self._q = deque(maxlen=max_size)

	@property
	def max_size(self):
		return self._q.maxlen

	def size(self):
		return len(self._q)

	def empty(self):
		return len(self._q) <= 0

	def put(self, item):
		self._q.append(item)

	def get(self):
		return self._q.popleft()

	def front(self):
		if not self._q:
			return None
		return self._q[0]

	def back(self):
		if not self._q:
			return None
		return self._q[-1]

	def remove(self, value):
		if value in self._q:
			self._q.remove(value)
