import json
import re
from django.shortcuts import render
from django.urls import resolve
from codebase_lib import config
from codebase_lib.constants import RunningEnvironment, AppType, ClientType
from codebase_lib.utils import api_response_error_params
from codebase_api.views import form_schema
from common.utils import get_timestamp

IGNORE_URL = ['/api/swagger', '/api/health', '/metrics', '/s2s/swagger']

API_PATTERN = {
	"url_pattern": "^/api/.*",
	"schema_pattern": ".*",
	"template": "index.html",
	"security": {
		"security": [{
			'user-token': []
		}],
		'securityDefinitions': {
			'user-token': {
				'type': 'apiKey',
				'in': 'header',
				'name': 'X-Cooky-User-Token'
			}
		}
	}
}

S2S_PATTERN = {
	"url_pattern": "^/s2s/.*",
	"schema_pattern": "S2S.*",
	"template": "index.html",
	"security": {}
}

def _gen_api_headers(app_id, client_type, client_version):
	timestamp = str(get_timestamp())
	headers = {
		'X-Cooky-App-Id': str(app_id),
		'X-Cooky-Client-Type': str(client_type),
		'X-Cooky-Client-Version': client_version,
		'X-Cooky-Client-Id': '0000',
		'X-Cooky-Timestamp': timestamp,
		'X-Cooky-Client-Language': 'vi',
		'Accept-Encoding': 'gzip',
		'content-encoding': 'gzip',
	}
	return headers

def _get_user_security():
	security = {
		'security': [{
			'user-token': []
		}],
		'securityDefinitions': {
			'user-token': {
				'type': 'apiKey',
				'in': 'header',
				'name': 'X-Cooky-User-Token'
			}
		}
	}
	return security

def _gen_s2s_headers(app_id):
	timestamp = str(get_timestamp())
	headers = {
		'X-App-Id': str(app_id),
		'Accept-Encoding': 'gzip',
		'content-encoding': 'gzip',
	}
	return headers


def api_index(request):
	return base_index(request, **API_PATTERN)

def s2s_index(request):
	return base_index(request, **S2S_PATTERN)

def base_index(request, url_pattern="*", schema_pattern="*", security={}, template="index.html"):
	if config.RUNNING_ENVIRONMENT in [RunningEnvironment.PRODUCTION, RunningEnvironment.STAGING]:
		return api_response_error_params()
	if config.RUNNING_ENVIRONMENT == RunningEnvironment.DEVELOPMENT:
		schemes = ['http']
	else:
		schemes = ['https']

	from codebase_api.urls import urlpatterns
	paths = {}
	definitions = {}
	app_id = 1000
	headers = _gen_s2s_headers(app_id)
	for urlpattern in urlpatterns:
		url_regex_pattern = urlpattern.pattern.regex.pattern
		url = "/" + url_regex_pattern.translate({ord(c): '' for c in "^$"})
		if url in IGNORE_URL:
			continue
		if not re.match(url_pattern, url):
			continue
		view_func, _, _ = resolve(url)
		view_schema = view_func.__dict__.get('schema')

		method = view_func.__dict__.get('method') or 'GET'
		request_schema = {"type": "object", "properties": {}}
		if view_schema:
			request_schema = view_schema.schema
		method = method.lower()
		parameters = []
		if request_schema.get('properties'):
			if method == 'post':
				parameters.append({
					'name': 'body',
					'in': 'body',
					'required': True,
					'schema': request_schema
				})
			if method == 'get':
				for field_name in request_schema.get('properties'):
					param = {
						'name': field_name,
						'in': 'query',
						'required': (request_schema.get('required') or []).append(field_name)
					}
					param.update(request_schema.get('properties').get(field_name, {}))
					parameters.append(param)
		tags = url.split('/')
		paths[url] = {
			method: {
				'tags': [tags[2] if tags[1] == 'api' else tags[1]],
				'parameters': parameters,
				'responses': {
					'200': {
						'description': 'successful operation',
						'schema': {'type': 'object'},
					}
				}
			}
		}

	for item in dir(form_schema):

		if 'Schema' not in item:
			continue
		if not re.match(schema_pattern, item):
			continue
		common_schema = getattr(form_schema, item)
		if isinstance(common_schema, dict):
			definitions[item] = common_schema

	swagger_info = {
		'swagger': '2.0',
		'info': {
			'title': 'Auth Api',
			'description': 'This is auth api for Cooky system.',
		},

		'schemes': schemes,
		'paths': paths,
		'definitions': definitions
	}
	if security:
		swagger_info.update(security)
	context = {
		'swagger_info': json.dumps(swagger_info),
		'headers': headers
	}
	return render(request, template, context)
