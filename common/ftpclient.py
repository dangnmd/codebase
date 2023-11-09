import sys
import socket
import ftplib
from ftplib import FTP, error_perm
from .logger import log


class CustomFTP(ftplib.FTP):
	def makepasv(self):
		if self.af == socket.AF_INET:
			host, port = ftplib.parse227(self.sendcmd('PASV'))
		else:
			host, port = ftplib.parse229(self.sendcmd('EPSV'), self.sock.getpeername())
		if '0.0.0.0' == host:
			""" this ip will be unroutable, we copy Filezilla and return the host instead """
			host = self.host
		return host, port

class FtpClient:

	def __init__(self, host, port, user, password, timeout):
		self._host = host
		self._port = port
		self._user = user
		self._password = password
		self._timeout = timeout
		self._ftp = None

	def listdir(self, path):
		if not self._connect():
			return []
		try:
			lines = []
			self._ftp.dir(path, lines.append)
			return lines
		except error_perm:
			self._close()
			log.exception('ftp_list_dir_error|path=%s', path)
		return []

	def rename(self, old_path, new_path):
		"""
		:param old_path:  ftp file path, e.g "/content/web_page/a.html"
		:param new_path:  ftp file path, e.g "/content/web_page/b.html"
		:return: True, False if failed
		"""
		if not self._connect():
			return False
		try:
			self._ftp.rename(old_path, new_path)
		except Exception as ex:
			log.exception('ftp_rename_error|old_path=%s,new_path=%s,ex=%s', old_path, new_path, ex)
			return False
		return True

	def download(self, path, f):
		"""
		:param path: ftp file path, e.g. "/content/web_page/a.html"
		:param f: output write file
		:return: True, False if failed
		"""
		if not self._connect():
			return False
		try:
			self._ftp.retrbinary("RETR %s" % path, f.write)
		except Exception as ex:
			log.exception('ftp_download_error|path=%s,ex=%s', path, ex)
			self._close()
			return False
		return True

	def upload(self, path, f):
		if not self._connect():
			return False
		try:
			if not path or not f:
				return False
			if path[0] != '/' or path[-1] == '/':
				return False
			i = path.rfind('/')
			in_dir = False
			while not in_dir and i > 0:
				try:
					self._ftp.cwd(path[:i])
					in_dir = True
				except Exception as ex:
					i = path.rfind('/', 0, i)
			i = path.find('/', i + 1)
			while i >= 0:
				self._ftp.mkd(path[:i])
				i = path.find('/', i + 1)
			self._ftp.storbinary('STOR ' + path, f)
			self._close()
		except Exception as ex:
			log.exception('ftp_upload_error|path=%s,ex=%s', path, ex)
			self._close()
			return False
		return True

	def upload_files(self, files):
		if not self._connect():
			return False
		try:
			for path in files:
				f = files[path]
				if not path or not f:
					self._close()
					return False
				if path[0] != '/' or path[-1] == '/':
					self._close()
					return False
				i = path.rfind('/')
				in_dir = False
				while not in_dir and i > 0:
					try:
						self._ftp.cwd(path[:i])
						in_dir = True
					except Exception as ex:
						i = path.rfind('/', 0, i)
				i = path.find('/', i + 1)
				while i >= 0:
					self._ftp.mkd(path[:i])
					i = path.find('/', i + 1)
				f.seek(0)
				self._ftp.storbinary('STOR ' + path, f)
		except Exception as ex:
			log.exception('ftp_upload_error|path=%s,ex=%s', path, ex)
			self._close()
			return False
		self._close()
		return True

	def _connect(self):
		try:
			if self._ftp is not None:
				self._close()
			self._ftp = CustomFTP()
			self._ftp.connect(self._host, self._port, self._timeout)
			self._ftp.login(self._user, self._password)
			self._ftp.set_pasv(True)
		except Exception as ex:
			log.exception('ftp_connect_error|ex=%s', ex)
			self._close()
			return False
		return True

	def _close(self):
		if self._ftp is not None:
			try:
				self._ftp.close()
				self._ftp = None
			except Exception as ex:
				log.exception('ftp_close_error|ex=%s', ex)
