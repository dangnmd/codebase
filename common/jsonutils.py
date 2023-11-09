try:
	import simplejson as json
except:
	import json

def to_json(data, ensure_ascii=False, ensure_bytes=False, default=None):
	result = json.dumps(data, ensure_ascii=ensure_ascii, separators=(',', ':'), default=default)
	if ensure_bytes and isinstance(result, str):
		result = result.encode('utf-8')
	return result

def from_json(s):
	return json.loads(s)

def from_json_safe(s):
	try:
		return json.loads(s)
	except:
		return None

_slash_escape = '\\/' in to_json('/')

def to_json_html_safe(obj, **kwargs):
	rv = to_json(obj, **kwargs)		\
		.replace('<', '\\u003c')	\
		.replace('>', '\\u003e')	\
		.replace('&', '\\u0026')	\
		.replace("'", '\\u0027')
	if isinstance(rv, str):
		rv = rv.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
	else:
		rv = rv.replace('\xe2\x80\xa8', '\\u2028').replace('\xe2\x80\xa8', '\\u2029')
	if _slash_escape:
		rv = rv.replace('\\/', '/')
	return rv
