import urllib.request, urllib.parse, urllib.error
import json
import io
import re

try:
	import pycurl
except ImportError:
	pycurl = None

try:
	import certifi
except ImportError:
	certifi = None

IP_REGEX = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')


class HttpResponse:
	def __init__(self, status_code, text):
		self.status_code = status_code
		self.text = text

	def json(self):
		return json.loads(self.text)


# Set shared curl options for both GET and POST
def set_curl_options(c, url, timeout, verify, cert, headers, client_cert):
	if timeout:
		c.setopt(pycurl.TIMEOUT, timeout)
		c.setopt(pycurl.CONNECTTIMEOUT, timeout)

	c.setopt(pycurl.FOLLOWLOCATION, 1)  # Follow redirects

	# Handle certificates
	if not verify:
		c.setopt(pycurl.SSL_VERIFYPEER, 0)
		c.setopt(pycurl.SSL_VERIFYHOST, 0)
	if cert is not None:
		c.setopt(pycurl.CAINFO, cert)
	elif verify and certifi:
		c.setopt(pycurl.CAINFO, certifi.where())

	# Client-side certificate
	if client_cert:
		if isinstance(client_cert, tuple) and len(client_cert) == 2:
			# Client cert as a pair tuple of paths to cert and key (assumed PEM format)
			# (client_cert, client_key)
			c.setopt(pycurl.SSLCERT, client_cert[0])
			c.setopt(pycurl.SSLKEY, client_cert[1])
		elif isinstance(client_cert, str):
			# Client cert is a path to file that combined cert and key
			c.setopt(pycurl.SSLCERT, client_cert)

	# Handle headers
	if headers:
		curl_headers = []
		hostname = None
		for key in headers:
			if key.lower() == "host":
				hostname = headers[key]
			curl_headers.append("%s: %s" % (key, headers[key]))
		c.setopt(pycurl.HTTPHEADER, curl_headers)

		# Handle SNI
		from urllib.parse import urlparse
		url_object = urlparse(url)
		if hasattr(pycurl, "RESOLVE") and hostname and IP_REGEX.match(url_object.hostname):
			default_port = 443 if url_object.scheme == "https" else 80
			port = url_object.port if url_object.port else default_port
			c.setopt(pycurl.RESOLVE, ["%s:%s:%s" % (hostname, port, url_object.hostname)])
			url = url.replace(url_object.hostname, hostname)

	c.setopt(pycurl.URL, url)


def http_get(url, params=None, timeout=None, verify=True, cert=None, headers=None, client_cert=None):
	if not pycurl:
		# Requests library fallback
		import requests
		verify_value = False if not verify else cert
		r = requests.get(url, params=params, timeout=timeout, verify=verify_value, cert=client_cert, headers=headers)
		return HttpResponse(r.status_code, r.content)

	c = pycurl.Curl()
	if params:
		params = urllib.parse.urlencode(params)
		url += '?' + params

	set_curl_options(c, url, timeout, verify, cert, headers, client_cert)

	b = io.StringIO()
	c.setopt(pycurl.WRITEFUNCTION, b.write)
	c.perform()
	return HttpResponse(c.getinfo(pycurl.HTTP_CODE), b.getvalue())


def http_post(url, data=None, timeout=None, verify=True, cert=None, headers=None, client_cert=None):
	if not pycurl:
		# Requests library fallback
		import requests
		verify_value = False if not verify else cert
		r = requests.post(url, data=data, timeout=timeout, verify=verify_value, cert=client_cert, headers=headers)
		return HttpResponse(r.status_code, r.content)

	c = pycurl.Curl()
	set_curl_options(c, url, timeout, verify, cert, headers, client_cert)

	c.setopt(pycurl.POST, 1)
	if data is not None:
		if isinstance(data, dict):
			data = urllib.parse.urlencode(data)
		c.setopt(pycurl.POSTFIELDS, data)
	b = io.StringIO()
	c.setopt(pycurl.WRITEFUNCTION, b.write)
	c.perform()
	return HttpResponse(c.getinfo(pycurl.HTTP_CODE), b.getvalue())
