import random
import struct
import platform
import socket
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.tcpserver import TCPServer
from .logger import log
from .simplequeue import SimpleQueue
from .utils import get_timestamp

IPV6_V4_PREFIX = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff'
IPV6_SIZE = 16
GTCP_PACKET_STUB_SIZE = 20
NOTIFY_SUCCESS = '\x00'
NOTIFY_FAILED = '\x01'
GTCP_CMD_SIZE = 1
GTCP_HEADER_SIZE = GTCP_CMD_SIZE + GTCP_PACKET_STUB_SIZE
GTCP_CMD_RELAY = '\x00'
GTCP_CMD_NONE = '\x01'
GTCP_CMD_ERROR = '\x02'
GTCP_CMD_CONNECT = '\x11'
GTCP_CMD_DISCONNECT = '\x12'

class TcpEndpoint(object):

	def __init__(self, client_id):
		self._client_id = client_id
		self._raw_ip = None
		self._ip = None
		self._ip_str = None
		self._port = None
		self._address = None
		self._parsed = False

	def __str__(self):
		return self.address

	def _parse(self):
		if self._parsed:
			return
		self._raw_ip = self._client_id[:IPV6_SIZE]
		(self._port,) = struct.unpack_from('!H', self._client_id, IPV6_SIZE)
		if self._raw_ip.startswith(IPV6_V4_PREFIX):
			ipv4 = self._raw_ip[len(IPV6_V4_PREFIX):]
			(self._ip,) = struct.unpack('!I', ipv4)
			self._ip_str = socket.inet_ntoa(ipv4)
		else:
			self._ip = self._raw_ip
			self._ip_str = socket.inet_ntop(socket.AF_INET6, self._raw_ip)
		self._address = '%s:%u' % (self._ip_str, self._port)
		self._parsed = True

	@property
	def id(self):
		return self._client_id

	@property
	def client_id(self):
		return self._client_id

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

class WorkerTask(object):
	def __init__(self, client, cmd, packet=''):
		self.client = client
		self.cmd = cmd
		self.packet = packet
		self.create_time = get_timestamp()

class GTcpConnection(object):

	HEADER_SIZE = 4

	def __init__(self, stream, address, config, on_packet=None, on_close=None):
		self._stream = stream
		self._address = address
		if stream.socket.family == socket.AF_INET6:
			self._remote_ip = socket.inet_pton(socket.AF_INET6, address[0])
		else:
			self._remote_ip = IPV6_V4_PREFIX + socket.inet_aton(address[0])
		self._remote_port = self._address[1]
		self._remote_address = '%s:%d' % address
		self._config = config
		if config.CONNECTION_ID_RANDOM_PADDING:
			padding = random.randint(0, 0xffff)
		else:
			padding = 0
		self._id = struct.pack('!16sHH', self._remote_ip, self._remote_port, padding)
		self._on_packet_callback = on_packet
		self._on_close_callback = on_close
		self._set_keep_alive()
		self._stream.set_close_callback(self._on_close)
		self._recv_header()
		self.running_task = None

	@property
	def id(self):
		return self._id

	@property
	def remote_address(self):
		return self._remote_address

	def closed(self):
		return self._stream.closed()

	def _set_keep_alive(self):
		if not self._config.ENABLE_KEEP_ALIVE:
			return
		stream_socket = self._stream.socket
		stream_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
		if platform.system().lower() == 'linux':
			stream_socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, self._config.KEEP_ALIVE_OPT['timeout'])
			stream_socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, self._config.KEEP_ALIVE_OPT['interval'])
			stream_socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, self._config.KEEP_ALIVE_OPT['count'])

	def send(self, data):
		self._stream.write(data)

	def send_packet(self, packet):
		header = struct.pack('<I', len(packet))
		try:
			self.send(header + packet)
		except:
			log.exception('tcp_conn_send_error|client_id=%s,remote=%s,packet=%s', self._id.encode('hex'), self._remote_address, packet.encode('hex'))
			self.close()

	def close(self):
		if not self._stream.closed():
			self._stream.close()

	def _recv_header(self):
		self._safe_recv(self.HEADER_SIZE, self._on_recv_header)

	def _on_recv_header(self, data):
		if len(data) != self.HEADER_SIZE:
			log.error('tcp_conn_header_size_error|id=%s,remote=%s,header=%s', self._id.encode('hex'), self._remote_address, data.encode('hex'))
			self._stream.close()
			return
		(body_size,) = struct.unpack('<I', data)
		if body_size >= self._config.TCP_MAX_PACKET_SIZE:
			log.error('tcp_conn_body_size_overflow|id=%s,remote=%s,size=%s', self._id.encode('hex'), self._remote_address, body_size)
			self._stream.close()
			return
		self._safe_recv(body_size, self._on_recv_body)

	def _on_recv_body(self, data):
		if self._on_packet_callback is not None:
			self._on_packet_callback(self, data)
		self._safe_recv(self.HEADER_SIZE, self._on_recv_header)

	def _safe_recv(self, size, callback):
		try:
			self._stream.read_bytes(size, callback)
		except:
			log.exception('tcp_conn_recv_error|id=%s,remote=%s,size=%s', self._id.encode('hex'), self._remote_address, size)
			self.close()

	def _on_close(self):
		if self._on_close_callback is not None:
			self._on_close_callback(self)

class CallbackTcpServer(TCPServer):

	def __init__(self, on_connect=None, *args, **kwargs):
		self._on_connect_callback = on_connect
		super(CallbackTcpServer, self).__init__(*args, **kwargs)

	def handle_stream(self, stream, address):
		if self._on_connect_callback:
			self._on_connect_callback(stream, address)

class Processor(object):

	NOTIFY_CLIENT_TIMEOUT = 3

	def __init__(self, id, config):	# pylint: disable=redefined-builtin
		self._id = id
		self._config = config
		self._notify_client = None

	def run(self):
		# pylint: disable=protected-access
		random.seed()
		self.on_process_init()
		thread_count = getattr(self._config, 'WORKER_THREAD_COUNT_PER_PROCESS', 1)
		if thread_count > 1:
			import threading
			worker_threads = []
			for i in range(thread_count):
				processor = self.__class__('%s.%s' % (self._id, i), self._config)
				t = threading.Thread(target=processor._run_worker)
				t.processor = processor
				t.start()
				worker_threads.append(t)
			for t in worker_threads:
				t.join()
		else:
			self._run_worker()

	def _run_worker(self):
		self.on_init()
		from .gtcpclient import GTcpClient
		log.info('tcp_worker_start|id=%s', self._id)
		notify_endpoint = getattr(self._config, 'NOTIFY_ENDPOINT', None)
		if notify_endpoint:
			self._notify_client = GTcpClient(notify_endpoint['address'], notify_endpoint['port'], self.NOTIFY_CLIENT_TIMEOUT)
		client = GTcpClient(self._config.WORK_ENDPOINT['address'], self._config.WORK_ENDPOINT['port'], 0)
		while True:
			try:
				request = client.receive()
				if request is None:
					log.warn('tcp_worker_lost_connection|id=%s', self._id)
					client.close()
				elif len(request) < GTCP_HEADER_SIZE:
					log.error('tcp_worker_request_packet_error|id=%s,request=%s', self._id, request.encode('hex'))
					client.close()
				else:
					request_cmd = request[:GTCP_CMD_SIZE]
					request_client = TcpEndpoint(request[GTCP_CMD_SIZE:GTCP_HEADER_SIZE])
					reply_body = None
					if request_cmd == GTCP_CMD_RELAY:
						request_body = request[GTCP_HEADER_SIZE:]
						reply_body = self.on_packet(request_client, request_body)
					elif request_cmd == GTCP_CMD_CONNECT:
						reply_body = self.on_client_connect(request_client)
					elif request_cmd == GTCP_CMD_DISCONNECT:
						self.on_client_disconnect(request_client)
					if reply_body is None:
						client.send(GTCP_CMD_NONE + request_client.client_id)
					else:
						client.send(GTCP_CMD_RELAY + request_client.client_id + reply_body)
			except Exception as ex:
				log.exception('tcp_worker_exception|id=%s,exception=%s', self._id, ex, exc_info=True)
				client.close()

	def run_background(self):
		random.seed()
		self.on_init()
		from .gtcpclient import GTcpClient
		log.info('tcp_background_worker_start|id=%s', self._id)
		notify_endpoint = getattr(self._config, 'NOTIFY_ENDPOINT', None)
		if notify_endpoint:
			self._notify_client = GTcpClient(notify_endpoint['address'], notify_endpoint['port'], self.NOTIFY_CLIENT_TIMEOUT)
		while True:
			try:
				self.on_background()
			except Exception as ex:
				log.exception('tcp_background_worker_exception|id=%s,exception=%s', self._id, ex, exc_info=True)

	def send_packet(self, client_id, packet):
		reply = self._notify_client.request(client_id + packet)
		return reply == NOTIFY_SUCCESS

	@property
	def id(self):
		return self._id

	def on_init(self):
		'''
		to be overridden
		'''
		return

	def on_process_init(self):
		'''
		to be overridden
		'''
		pass

	def on_packet(self, client, request):
		'''
		to be overridden
		'''
		return ''

	def on_client_connect(self, client):
		'''
		to be overridden
		'''
		return

	def on_client_disconnect(self, client):
		'''
		to be overridden
		'''
		return

	def on_background(self):
		'''
		to be overridden
		'''
		return

def _start_processor(processor_class, processor_id, config, func_name):
	processor = processor_class(processor_id, config)
	getattr(processor, func_name)()

class GTcpServer(object):

	DEFAULT_TASK_TIMEOUT = None # in seconds, None means never timeout

	def __init__(self, config, processor_class):
		if config.DEBUG:
			from threading import Thread as Process
		else:
			from multiprocessing import Process

		max_buffer_size = getattr(config, 'TCP_MAX_BUFFER_SIZE', None)
		notify_endpoint = getattr(config, 'NOTIFY_ENDPOINT', None)
		task_timeout = getattr(config, 'TASK_TIMEOUT', GTcpServer.DEFAULT_TASK_TIMEOUT)

		self._config = config
		self._clients = {}
		self._idle_workers = SimpleQueue()
		self._running_workers = set()
		self._waiting_tasks = SimpleQueue()
		self._background_processes = []
		self._worker_processes = []
		self._task_timeout = task_timeout

		if notify_endpoint:
			self._notify_server = CallbackTcpServer(on_connect=self._on_notify_connect, max_buffer_size=max_buffer_size)
			self._notify_server.listen(**notify_endpoint)
		self._worker_server = CallbackTcpServer(on_connect=self._on_worker_connect, max_buffer_size=max_buffer_size)
		self._worker_server.listen(**config.WORK_ENDPOINT)
		self._client_server = CallbackTcpServer(on_connect=self._on_client_connect, max_buffer_size=max_buffer_size)
		for listen_port in config.LISTEN_ENDPOINTS:
			self._client_server.listen(**listen_port)
		for i in range(0, getattr(config, 'BACKGROUND_WORKER_COUNT', 0)):
			p = Process(target=_start_processor, args=(processor_class, i, config, 'run_background'))
			self._background_processes.append(p)
			p.start()
		if hasattr(config, 'WORKER_PROCESS_COUNT'):
			process_count = config.WORKER_PROCESS_COUNT
		else:
			process_count = config.WORKER_COUNT
		for i in range(process_count):
			p = Process(target=_start_processor, args=(processor_class, i, config, 'run'))
			self._worker_processes.append(p)
			p.start()
		PeriodicCallback(self._log_status, 5000).start()

	def _on_client_connect(self, stream, address):
		client = GTcpConnection(stream, address, self._config, self._on_client_packet, self._on_client_close)
		if client.id in self._clients:
			log.error('tcp_server_dup_client|id=%s,remote=%s', client.id.encode('hex'), client.remote_address)
		self._clients[client.id] = client
		self._handle_task(client, GTCP_CMD_CONNECT, '')
		log.info('tcp_server_client_connect|id=%s,remote=%s', client.id.encode('hex'), client.remote_address)

	def _on_worker_connect(self, stream, address):
		worker = GTcpConnection(stream, address, self._config, self._on_worker_packet, self._on_worker_close)
		worker.running_task = None
		log.info('tcp_server_worker_connect|id=%s,remote=%s', worker.id.encode('hex'), worker.remote_address)
		self._on_worker_idle(worker)

	def _on_notify_connect(self, stream, address):
		worker = GTcpConnection(stream, address, self._config, self._on_notify_packet)
		log.info('tcp_server_notify_connect|id=%s,remote=%s', worker.id.encode('hex'), worker.remote_address)

	def _handle_task(self, client, cmd, data=''):
		task = WorkerTask(client, cmd, data)
		if self._idle_workers.empty():
			self._waiting_tasks.put(task)
		else:
			self._assign_task(self._idle_workers.get(), task)

	def _on_client_packet(self, client, data):
		self._handle_task(client, GTCP_CMD_RELAY, data)

	def _on_client_close(self, client):
		log.info('tcp_server_client_close|id=%s,remote=%s', client.id.encode('hex'), client.remote_address)
		if client.id not in self._clients:
			log.error('tcp_server_close_conn_not_found|id=%s,remote=%s', client.id.encode('hex'), client.remote_address)
			return
		self._handle_task(client, GTCP_CMD_DISCONNECT, '')
		del self._clients[client.id]

	def _on_worker_packet(self, worker, data):
		client = worker.running_task.client
		packet_size = len(data)
		if packet_size < GTCP_HEADER_SIZE:
			log.error('tcp_worker_reply_error|client_id=%s,client=%s,reply=%s', client.id.encode('hex'), client.remote_address, data.encode('hex'))
			worker.running_task.client.close()
			worker.close()
			return
		reply_cmd = data[:1]
		if reply_cmd == GTCP_CMD_RELAY:
			reply_client = data[GTCP_CMD_SIZE:GTCP_HEADER_SIZE]
			reply_data = data[GTCP_HEADER_SIZE:]
			if reply_client in self._clients:
				self._clients[reply_client].send_packet(reply_data)
			else:
				log.error('tcp_reply_client_not_found|client_id=%s,reply=%s', reply_client.encode('hex'), reply_data.encode('hex'))
				worker.running_task.client.close()
		self._on_worker_idle(worker)

	def _on_worker_close(self, worker):
		if worker.running_task is not None:
			worker.running_task.client.close()
		self._idle_workers.remove(worker)
		self._remove_running_worker(worker)

	def _on_notify_packet(self, client, data):
		packet_size = len(data)
		if packet_size < GTCP_PACKET_STUB_SIZE:
			log.error('tcp_notify_request_error|remote_id=%s,remote=%s,notify=%s', client.id.encode('hex'), client.remote_address, data)
			client.close()
			return
		notify_client = data[:GTCP_PACKET_STUB_SIZE]
		if notify_client not in self._clients:
			log.error('tcp_notify_client_not_found|client_id=%s,reply=%s', notify_client.encode('hex'), data[GTCP_PACKET_STUB_SIZE:].encode('hex'))
			client.send_packet(NOTIFY_FAILED)
			return
		self._clients[notify_client].send_packet(data[GTCP_PACKET_STUB_SIZE:])
		client.send_packet(NOTIFY_SUCCESS)

	def _on_worker_idle(self, worker):
		current_ts = get_timestamp()
		while not self._waiting_tasks.empty():
			task = self._waiting_tasks.get()
			if task.cmd == GTCP_CMD_RELAY and self._task_timeout is not None and current_ts - task.create_time > self._task_timeout:
				log.warn("tcp_drop_timeout_packet|remote_id=%s,remote=%s,packet_ts=%s,current_ts=%s,packet_data=%s", task.client.id.encode('hex'),
					task.client.remote_address, task.create_time, current_ts, task.packet.encode("hex"))
			else:
				self._assign_task(worker, task)
				return
		self._remove_running_worker(worker)
		self._idle_workers.put(worker)

	def _assign_task(self, worker, task):
		self._running_workers.add(worker)
		worker.running_task = task
		worker.send_packet(task.cmd + task.client.id + task.packet)

	def _remove_running_worker(self, worker):
		if worker in self._running_workers:
			self._running_workers.remove(worker)

	def _log_status(self):
		delay = 0
		if self._waiting_tasks.size() > 0:
			delay = get_timestamp() - self._waiting_tasks.front().create_time
		log.info('tcp_server_status|running=%s,idle=%s,waiting=%s,delay=%s',
			len(self._running_workers), self._idle_workers.size(), self._waiting_tasks.size(), delay)

def run():
	IOLoop.instance().start()
