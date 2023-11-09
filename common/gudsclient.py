import socket
from .logger import log

from .gtcpclient import GTcpClient


class GUdsClient(GTcpClient):

	def __init__(self, address, timeout=10, retry=True, on_connect=None, on_disconnect=None):
		super(GUdsClient, self).__init__(address, None, timeout, retry, on_connect, on_disconnect)

	def _connect(self):
		try:
			self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
			if self._timeout > 0:
				self._socket.settimeout(self._timeout)
			self._socket.connect(self._address)
			log.info('tcp_connect|address=%s,port=%u', self._address, self._port)
			self._on_connect()
			return True
		except Exception as ex:
			log.exception('tcp_connect_fail|address=%s,port=%u,ex=%s', self._address, self._port, ex)
			self.close()
			return False
