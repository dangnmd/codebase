import socket
from .logger import log

class UdpClient(object):

	UDP_MAX_PACKET_SIZE = 65507

	def __init__(self, address, port, timeout=10, max_packet_size=None):
		self._address = address
		self._port = port
		self._socket = None
		self._timeout = timeout
		self._max_packet_size = max_packet_size or self.UDP_MAX_PACKET_SIZE

	def close(self):
		if self._socket is not None:
			self._socket.close()
			self._socket = None

	# return the number of bytes sent
	def send(self, packet):
		if self._socket is None and not self._open():
			return 0
		try:
			return self._socket.sendto(packet, (self._address, self._port))
		except Exception as ex:
			log.exception('udp_send_fail|address=%s,port=%u,ex=%s', self._address, self._port, ex)
			return 0

	def receive(self):
		if self._socket is None and not self._open():
			return None
		try:
			return self._socket.recv(self._max_packet_size)
		except Exception as ex:
			log.exception('udp_receive_fail|address=%s,port=%u,ex=%s', self._address, self._port, ex)
			return None

	def _open(self):
		try:
			self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			if self._timeout > 0:
				self._socket.settimeout(self._timeout)
			return True
		except Exception as ex:
			log.exception('udp_open_socket_fail|address=%s,port=%u,ex=%s', self._address, self._port, ex)
			self.close()
			return False
