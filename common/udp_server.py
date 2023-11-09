# pylint: disable=wildcard-import
import os
import errno
import socket
import collections
from tornado.ioloop import IOLoop
from tornado.platform.auto import set_close_exec
from tornado.util import errno_from_exception
from tornado import process
from .utils import get_timestamp

# ---- UDP SERVER ASYNC BASED ON IOLOOP ----

class UDPSocketInfo(object):

	def __init__(self, sock, max_sending_buffer_size):
		self.sock = sock
		self.sending_buff_size = 0
		self.sending_buff = collections.deque()
		self._max_sending_buffer_size = max_sending_buffer_size

	def append_sending_packet(self, client_address, packet):
		packet_size = len(packet)
		if packet_size == 0:
			return
		if (self.sending_buff_size + packet_size > self._max_sending_buffer_size):
			log.warn('sending_buffer_overflow|sock_id=%d', self.sock.fileno())
			# clear buffer
			self.sending_buff.clear()
			self.sending_buff_size = 0
		self.sending_buff.append((client_address, packet))
		self.sending_buff_size += packet_size

	def top_sending_packet(self):
		if not self.sending_buff:
			return None, None
		return self.sending_buff[0]

	def pop_sending_packet(self):
		if not self.sending_buff:
			return None, None
		address, packet = self.sending_buff.popleft()
		self.sending_buff_size -= len(packet)
		return address, packet

	def clear(self):
		self.sock.close()
		self.sending_buff_size = 0
		self.sending_buff.clear()

class UDPServer(object):

	UDP_MAX_PACKET_SIZE = 65507
	MAX_SENDING_BUFFER_SIZE = 1024 * 1024

	def __init__(self, on_packet, max_packet_size=None, max_sending_buffer_size=None, io_loop=None):
		self.io_loop = io_loop or IOLoop.current()
		self._sockets = {}  # fd -> UDPSocketInfo
		self._pending_sockets = []
		self._started = False
		self._on_packet = on_packet
		self._max_packet_size = max_packet_size or self.UDP_MAX_PACKET_SIZE
		self._max_sending_buffer_size = max_sending_buffer_size or self.MAX_SENDING_BUFFER_SIZE

	@staticmethod
	def bind_udp_sockets(port, address=None, family=socket.AF_UNSPEC, backlog=128, flags=None):
		sockets = []
		if address == "":
			address = None
		if not socket.has_ipv6 and family == socket.AF_UNSPEC:
			family = socket.AF_INET
		if flags is None:
			flags = socket.AI_PASSIVE
		bound_port = None
		for res in set(socket.getaddrinfo(address, port, family, socket.SOCK_DGRAM, 0, flags)):
			af, socket_type, protocol, _canonname, socket_addr = res
			try:
				sock = socket.socket(af, socket_type, protocol)
			except socket.error as e:
				if errno_from_exception(e) == errno.EAFNOSUPPORT:
					continue
				raise
			set_close_exec(sock.fileno())
			if os.name != 'nt':
				sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			if af == socket.AF_INET6:
				if hasattr(socket, "IPPROTO_IPV6"):
					sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)

			host, requested_port = socket_addr[:2]
			if requested_port == 0 and bound_port is not None:
				socket_addr = tuple([host, bound_port] + list(socket_addr[2:]))

			sock.setblocking(0)
			sock.bind(socket_addr)
			bound_port = sock.getsockname()[1]
			sockets.append(sock)
		return sockets

	def _read_packet(self, sock_info):
		try:
			packet, client_address = sock_info.sock.recvfrom(self._max_packet_size)
		except socket.error as e:
			if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
				log.exception('socket_receive_fail|error=%s', e)
			return False
		self._on_packet(sock_info.sock.family, sock_info.sock.fileno(), client_address, packet, self)
		return True

	def _write_packet(self, sock_info):
		address, packet = sock_info.top_sending_packet()
		try:
			sent_size = sock_info.sock.sendto(packet, address)
		except socket.error:
			log.exception('socket_send_fail|address=%s, packet=%s', address, packet.encode('hex'))
			return False
		packet_size = len(packet)
		if sent_size != packet_size:
			log.warn('socket_send_fail|address=%s,packet_size=%d,sent_size=%d', address, packet_size, sent_size)
			return False
		sock_info.pop_sending_packet()
		return True

	def on_event(self, fd, events):
		sock_info = self._sockets.get(fd)
		if sock_info is None:
			log.error('socket_fd_not_exist|fd=%d', fd)
			return
		is_read = events & self.io_loop.READ
		is_write = events & self.io_loop.WRITE
		while is_read or is_write:
			if is_read:
				is_read = self._read_packet(sock_info)
			if is_write:
				if not sock_info.sending_buff:
					self.io_loop.update_handler(fd, IOLoop.READ)
					is_write = False
				else:
					is_write = self._write_packet(sock_info)

	def add_sockets(self, sockets):
		if self.io_loop is None:
			self.io_loop = IOLoop.current()

		for sock in sockets:
			self._sockets[sock.fileno()] = UDPSocketInfo(sock, self._max_sending_buffer_size)
			self.io_loop.add_handler(sock.fileno(), self.on_event, IOLoop.READ)

	def listen(self, port, address=None):
		sockets = self.bind_udp_sockets(port, address=address)
		self.add_sockets(sockets)

	def bind(self, port, address=None, family=socket.AF_UNSPEC, backlog=128):
		sockets = self.bind_udp_sockets(port, address=address, family=family, backlog=backlog)
		if self._started:
			self.add_sockets(sockets)
		else:
			self._pending_sockets.extend(sockets)

	def start(self, num_processes=1):
		assert not self._started
		self._started = True
		if num_processes != 1:
			process.fork_processes(num_processes)
		sockets = self._pending_sockets
		self._pending_sockets = []
		self.add_sockets(sockets)

	def stop(self):
		for fd, sock_info in list(self._sockets.items()):
			self.io_loop.remove_handler(fd)
			sock_info.clear()

	def send(self, sock_id, client_address, packet):
		sock_info = self._sockets.get(sock_id)
		if sock_info is None:
			log.error('socket_fd_not_exist|sock_id=%d', sock_id)
			return False
		sock_info.append_sending_packet(client_address, packet)
		self.io_loop.update_handler(sock_id, IOLoop.READ | IOLoop.WRITE)
		return True

# --- GUDP SERVER: UDP Server & TCP connection to worker

from .tcp_server import *	# pylint: disable=wrong-import-position

class UdpEndpoint(object):

	def __init__(self, sock_family, sock_id, address, client_id=None):
		self.sock_family = sock_family
		self.sock_id = sock_id
		self.address = address
		self._client_id = client_id

	@property
	def client_id(self):
		if self._client_id is None:
			#create id
			if self.sock_family == socket.AF_INET6:
				remote_ip = socket.inet_pton(socket.AF_INET6, self.address[0])
			else:
				remote_ip = IPV6_V4_PREFIX + socket.inet_aton(self.address[0])
			remote_port = self.address[1]
			self._client_id = struct.pack('!16sHH', remote_ip, remote_port, self.sock_id)
		return self._client_id

	@classmethod
	def from_id(cls, client_id):
		raw_ip = client_id[:IPV6_SIZE]
		port, sock_id = struct.unpack_from('!HH', client_id, IPV6_SIZE)
		if raw_ip.startswith(IPV6_V4_PREFIX):
			socket_family = socket.AF_INET
			ipv4 = raw_ip[len(IPV6_V4_PREFIX):]
			ip_str = socket.inet_ntoa(ipv4)
		else:
			socket_family = socket.AF_INET6
			ip_str = socket.inet_ntop(socket.AF_INET6, raw_ip)
		address = (ip_str, port)
		return cls(socket_family, sock_id, address, client_id)


class UdpWorkerTask(object):

	def __init__(self, endpoint, packet):
		self.endpoint = endpoint
		self.packet = packet
		self.create_time = get_timestamp()

class GUdpServer(object):

	DEFAULT_TASK_QUEUE_MAX_SIZE = 10000
	DEFAULT_TASK_TIMEOUT = None # in seconds - None means never time out

	def __init__(self, config, processor_class):
		if config.DEBUG:
			from threading import Thread as Process
		else:
			from multiprocessing import Process

		udp_max_packet_size = getattr(config, 'UDP_MAX_PACKET_SIZE', None)
		udp_max_sending_buffer_size = getattr(config, 'UDP_MAX_SENDING_BUFFER_SIZE', None)
		tcp_max_buffer_size = getattr(config, 'TCP_MAX_BUFFER_SIZE', None)
		task_queue_max_size = getattr(config, 'TASK_QUEUE_MAX_SIZE', GUdpServer.DEFAULT_TASK_QUEUE_MAX_SIZE)
		task_timeout = getattr(config, 'TASK_TIMEOUT', GUdpServer.DEFAULT_TASK_TIMEOUT)

		self._config = config
		self._clients = {}
		self._idle_workers = SimpleQueue()
		self._running_workers = SimpleQueue()
		self._waiting_tasks = SimpleQueue()
		self._worker_processes = []
		self._task_timeout = task_timeout
		self._task_queue_max_size = task_queue_max_size

		notify_endpoint = getattr(config, 'NOTIFY_ENDPOINT', None)
		if notify_endpoint:
			self._notify_server = CallbackTcpServer(on_connect=self._on_notify_connect, max_buffer_size=tcp_max_buffer_size)
			self._notify_server.listen(**notify_endpoint)

		self._worker_server = CallbackTcpServer(on_connect=self._on_worker_connect, max_buffer_size=tcp_max_buffer_size)
		self._worker_server.listen(**config.WORK_ENDPOINT)

		self._client_server = UDPServer(self._on_client_packet, udp_max_packet_size, udp_max_sending_buffer_size)
		for listen_endpoint in config.LISTEN_ENDPOINTS:
			self._client_server.listen(**listen_endpoint)

		for i in range(0, config.WORKER_COUNT):
			processor = processor_class(i, config)
			p = Process(target=processor.run)
			p.processor = processor
			self._worker_processes.append(p)
			p.start()

	def _on_notify_connect(self, stream, address):
		worker = GTcpConnection(stream, address, self._config, self._on_notify_packet)
		log.info('udp_server_notify_connect|id=%s,remote=%s', worker.id.encode('hex'), worker.remote_address)

	def _on_notify_packet(self, client, data):
		packet_size = len(data)
		if packet_size < GTCP_PACKET_STUB_SIZE:
			log.error('udp_notify_request_error|remote_id=%s,remote=%s,notify=%s', client.id.encode('hex'), client.remote_address, data)
			client.close()
			return
		notify_endpoint_id = data[:GTCP_PACKET_STUB_SIZE]
		notify_endpoint = UdpEndpoint.from_id(notify_endpoint_id)
		if self._client_server.send(notify_endpoint.sock_id, notify_endpoint.address, data[GTCP_PACKET_STUB_SIZE:]):
			client.send_packet(NOTIFY_SUCCESS)
		else:
			log.error('udp_notify_send_error|notify_endpoint_address=%s,data=%s', notify_endpoint.address, data.encode('hex'))
			client.send_packet(NOTIFY_FAILED)

	def _on_worker_connect(self, stream, address):
		worker = GTcpConnection(stream, address, self._config, self._on_worker_packet, self._on_worker_close)
		worker.running_task = None
		log.info('udp_server_worker_connect|id=%s,remote=%s', worker.id.encode('hex'), worker.remote_address)
		self._on_worker_idle(worker)

	def _on_worker_close(self, worker):
		self._idle_workers.remove(worker)
		self._running_workers.remove(worker)

	def _on_worker_packet(self, worker, data):
		client_endpoint = worker.running_task.endpoint
		packet_size = len(data)
		if packet_size < GTCP_HEADER_SIZE:
			log.error('udp_worker_reply_error|client_id=%s,client=%s,reply=%s', client_endpoint.id.encode('hex'), client_endpoint.address, data)
			worker.running_task.client.close()
			return

		reply_cmd = data[:GTCP_CMD_SIZE]
		if reply_cmd == GTCP_CMD_RELAY:
			reply_endpoint_id = data[GTCP_CMD_SIZE:GTCP_HEADER_SIZE]
			reply_data = data[GTCP_HEADER_SIZE:]
			reply_endpoint = UdpEndpoint.from_id(reply_endpoint_id)
			if not self._client_server.send(reply_endpoint.sock_id, reply_endpoint.address, reply_data):
				log.error('udp_worker_reply_send_error|reply_endpoint_address=%s,data=%s', reply_endpoint.address, data.encode('hex'))
		self._on_worker_idle(worker)

	def _on_worker_idle(self, worker):
		current_ts = get_timestamp()
		while not self._waiting_tasks.empty():
			task = self._waiting_tasks.get()
			if self._task_timeout is not None and current_ts - task.create_time > self._task_timeout:
				log.warn("udp_drop_timeout_packet|packet_endpoint=%s,packet_ts=%s,current_ts=%s,packet_data=%s",
					task.endpoint.address, task.create_time, current_ts, task.packet.encode('hex'))
			else:
				self._assign_task(worker, task)
				return
		self._idle_workers.put(worker)

	def _on_client_packet(self, socket_family, socket_id, client_address, packet, server):
		task = UdpWorkerTask(UdpEndpoint(socket_family, socket_id, client_address), packet)
		if self._idle_workers.empty():
			if self._waiting_tasks.size() > self._task_queue_max_size:
				drop_task = self._waiting_tasks.get()
				log.warn("udp_full_queue_drop_task|packet_endpoint=%s,packet_ts=%s,packet_data=%s",
					drop_task.endpoint.address, drop_task.create_time, drop_task.packet.encode('hex'))
			self._waiting_tasks.put(task)
		else:
			self._assign_task(self._idle_workers.get(), task)

	def _assign_task(self, worker, task):
		worker.running_task = task
		worker.send_packet(GTCP_CMD_RELAY + task.endpoint.client_id + task.packet)
		self._running_workers.put(worker)
