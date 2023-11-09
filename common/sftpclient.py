import os
import pysftp
from pysftp import ConnectionException
from paramiko.ssh_exception import SSHException
from .logger import log


class SFtpClient:
	SFTP_CONNECTION_EXCEPTIONS = (IOError, ConnectionException, SSHException)

	def __init__(self, host, port=None, username=None, password=None, private_key=None):
		conn_info = {'host': host}
		if port is not None:
			conn_info['port'] = port
		if username is not None:
			conn_info['username'] = username
		if password is not None:
			conn_info['password'] = password
		if private_key is not None:
			conn_info['private_key'] = private_key
		self._conn_info = conn_info
		self._conn = None

	def _check_path_format(self, path, is_file=False):
		"""
		:param path:
			should be of format /parent_dir/dir/filename, if is_file = True
			should be of format /parent_dir/dir/ or /parent_dir/dir, otherwise
		"""
		if not (path and path[0] == "/" and (not is_file or path[-1] != "/")):
			log.warning('check_path_format_error|host=%s,path=%s,is_file=%s', self._conn_info['host'], path, is_file)
			return False
		return True

	def isfile(self, remote_path):
		self._check_connection()
		return self._conn.isfile(remote_path)

	def isdir(self, remote_path):
		self._check_connection()
		return self._conn.isdir(remote_path)

	def mkdir(self, remote_path):
		"""
		:param remote_path: should be of format /parent_dir/dir/ or /parent_dir/dir
		"""
		if not self._check_path_format(remote_path, is_file=False):
			return False
		try:
			self._check_connection()
			if remote_path[-1] != "/":
				remote_path += "/"
			if self.isdir(remote_path):
				return True
			dirs = []
			current_dir, _ = os.path.split(remote_path)
			while len(current_dir) > 1:
				if self.isdir(current_dir):
					break
				dirs.append(current_dir)
				current_dir, _ = os.path.split(current_dir)
			while dirs:
				current_dir = dirs.pop()
				self._conn.mkdir(current_dir)
			return True
		except self.SFTP_CONNECTION_EXCEPTIONS:
			log.exception('sftp_connection_exceptions|host=%s,remote_path=%s', self._conn_info['host'], remote_path)
			self._close()
		return False

	def upload_file(self, local_path, remote_path):
		"""
		:param remote_path: should be of format /parent_dir/dir/filename
		"""
		if not self._check_path_format(remote_path, is_file=True):
			return False
		try:
			self._check_connection()
			remote_dir, _ = os.path.split(remote_path)
			if self.mkdir(remote_dir):
				self._conn.put(local_path, remote_path)
				return True
		except self.SFTP_CONNECTION_EXCEPTIONS:
			log.exception('sftp_connection_exceptions|host=%s,local_path=%s,remote_path=%s', self._conn_info['host'], local_path, remote_path)
			self._close()
		return False

	def download_file(self, remote_path, local_path):
		"""
		:param remote_path: should be of format /parent_dir/dir/filename
		:param local_path: should be of format /parent_dir/dir/filename
		"""
		if not self._check_path_format(local_path, is_file=True):
			return False
		try:
			self._check_connection()
			local_dir, _ = os.path.split(local_path)
			if not os.path.exists(local_dir):
				os.makedirs(local_dir)
			self._conn.get(remote_path, local_path)
			return True
		except self.SFTP_CONNECTION_EXCEPTIONS:
			log.exception('sftp_connection_exceptions|host=%s,remote_path=%s,local_path=%s', self._conn_info['host'], remote_path, local_path)
			self._close()
		return False

	get_file = download_file

	def upload(self, file_object, remote_path):
		"""
		:param remote_path: should be of format /parent_dir/dir/filename
		"""
		if not self._check_path_format(remote_path, is_file=True):
			return False
		try:
			self._check_connection()
			remote_dir, _ = os.path.split(remote_path)
			if self.mkdir(remote_dir):
				self._conn.putfo(file_object, remote_path)
				return True
		except self.SFTP_CONNECTION_EXCEPTIONS:
			log.exception('sftp_connection_exceptions|host=%s,file_object=%s,remote_path=%s', self._conn_info['host'], file_object, remote_path)
			self._close()
		return False

	def remove_file(self, remote_path):
		"""
		:param remote_path: should be of format /parent_dir/dir/filename
		"""
		if not self._check_path_format(remote_path, is_file=True):
			return False
		try:
			self._check_connection()
			if not self.isfile(remote_path):
				log.warning('remote_path_not_a_file|host=%s,remote_path=%s', self._conn_info['host'], remote_path)
				return True
			self._conn.remove(remote_path)
			return True
		except self.SFTP_CONNECTION_EXCEPTIONS:
			log.exception('sftp_connection_exceptions|host=%s,remote_path=%s', self._conn_info['host'], remote_path)
			self._close()
		return False

	def cd(self, remote_path):
		try:
			self._check_connection()
			self._conn.cd(remote_path)
			return True
		except self.SFTP_CONNECTION_EXCEPTIONS:
			log.exception('sftp_connection_exceptions|host=%s,remote_path=%s', self._conn_info['host'], remote_path)
			self._close()
		return False

	def listdir(self, remote_path):
		"""
		:param remote_path: should be of format /parent_dir/dir/ or /parent_dir/dir
		:return [remote_file_path, ...]
		"""
		if not self._check_path_format(remote_path, is_file=False):
			return []
		try:
			self._check_connection()
			return self._conn.listdir(remote_path)
		except self.SFTP_CONNECTION_EXCEPTIONS:
			log.exception('sftp_connection_exceptions|host=%s,remote_path=%s', self._conn_info['host'], remote_path)
			self._close()
		return []

	ls = listdir

	def rename(self, remote_src, remote_dest):
		"""
		:param remote_src: should be of format /parent_dir/dir/[filename|dir] or /parent_dir/dir/
		:param remote_dest: should be of format /parent_dir/dir/[filename|dir] or /parent_dir/dir/
		"""
		if not self._check_path_format(remote_src):
			return False
		if not self._check_path_format(remote_dest):
			return False
		try:
			self._check_connection()
			self._conn.rename(remote_src, remote_dest)
			return True
		except self.SFTP_CONNECTION_EXCEPTIONS:
			log.exception('sftp_connection_exceptions|host=%s,remote_src=%s,remote_dest=%s', self._conn_info['host'], remote_src, remote_dest)
			self._close()
		return False

	def close(self):
		self._close()

	def _close(self):
		if self._conn is not None:
			try:
				self._conn.close()
			except:
				log.exception('sftp_close_connection_error|host=%s', self._conn_info['host'])
			self._conn = None

	def _connect(self):
		self._conn = pysftp.Connection(**self._conn_info)

	def _check_connection(self):
		if self._conn is None:
			self._connect()
