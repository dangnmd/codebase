import struct
import socket

class GClientStub(object):

	STUB_SIZE = 8

	def __init__(self, data):
		self._data = data[:self.STUB_SIZE]
		self._ip = None
		self._port = None
		self._tag = None
		self._ip_str = None
		self._address = None
		self._parsed = False

	def __str__(self):
		return self.address

	def _parse(self):
		if self._parsed:
			return
		self._ip, self._port, self._tag = struct.unpack('<IHH', self._data)
		self._ip_str = socket.inet_ntoa(struct.pack('!I', self._ip))
		self._address = '%s:%u(%u)' % (self._ip_str, self._port, self._tag)
		self._parsed = True

	@property
	def client_id(self):
		return self._data

	@property
	def address(self):
		self._parse()
		return self._address

	@property
	def ip(self):
		self._parse()
		return self._ip

	@property
	def port(self):
		self._parse()
		return self._port
