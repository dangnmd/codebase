import ssl
import socket
from .logger import log
from .gtcpclient import GTcpClient

class GTlsClient(GTcpClient):

	def __init__(self, address, port, timeout=0, retry=True, cert=None, on_connect=None, on_disconnect=None):
		super(GTlsClient, self).__init__(address, port, timeout, retry, on_connect, on_disconnect)
		self._cert = cert
		self._tcp_socket = None

	def close(self):
		if self._socket is not None:
			self._socket.close()
			self._socket = None
			self._tcp_socket = None
			self._on_disconnect()

	def _connect(self):
		try:
			self._tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			if self._timeout > 0:
				self._tcp_socket.settimeout(self._timeout)
			self._socket = ssl.wrap_socket(self._tcp_socket, ca_certs=self._cert, cert_reqs=ssl.CERT_REQUIRED, server_side=False)
			self._socket.connect((self._address, self._port))
			log.info('tcp_connect|address=%s,port=%u', self._address, self._port)
			self._on_connect()
			return True
		except Exception as ex:
			log.exception('tcp_connect_fail|address=%s,port=%u,ex=%s', self._address, self._port, ex)
			self.close()
			return False
