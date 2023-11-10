from codebase_lib.constants import AppType, RunningEnvironment, ServiceType
import os


RUNNING_ENVIRONMENT = RunningEnvironment.DEVELOPMENT
DEBUG = False
TESTING = True

COUNTRY = 'VN'
LANGUAGE = 'en'
# GEOIP_PATH = "/opt/ip2location/ip-country.bin"

ALLOWED_HOSTS = ['*']

solr_host = 'demosolr.cooky.vn:8982'
if os.environ.get('SOLR_HOST'):
	solr_host = os.environ.get('SOLR_HOST')

SOLR_ENDPOINT = {
	'url': 'http://%s/solr/place' % solr_host
}

SOLR_ENDPOINT_PLAN = {
	'url': 'http://%s/solr/plan' % solr_host
}

SENTRY_DSN = "http://658f1e70fd3f4b82a66415db1275789a@sentry.cooky.com.vn:9000/3"#"https://cc69f2417595407980e8ffc2b4ea7497@sentry.cooky.com.vn/61"

METRICS_DATA_LOCATION = "/data/prometheus/%s"
METRICS_IP_WHITELIST = (
	'127.0.0.1',
	'210.211.116.165',  # vpn
)

CACHE_SERVERS = {
	"default": {
		"type": "redis",
		"host": "redis.demo.cooky.com.vn",
		"port": 6379,
		"default_timeout": 604800,
		'key_prefix': 'codebase_dev.'
	},
}


DATABASE_BACKEND = "django"
DATABASES = {
	'default': {
		'NAME': 'dnguyen_api',
		'ENGINE': 'django.db.backends.mysql',
		'HOST': '172.17.0.2',
		'PORT': '3306',
		'USER': 'root',
		'PASSWORD': 'dnguyen_api_mysql3306123456',
		'CONN_MAX_AGE': 3600,
		'OPTIONS': {'charset': 'utf8mb4'},
	},
	'dnguyen_db.master': {
		'NAME': 'dnguyen_api',
		'ENGINE': 'django.db.backends.mysql',
		'HOST': '172.17.0.2',
		'PORT': '3306',
		'USER': 'root',
		'PASSWORD': 'dnguyen_api_mysql3306123456',
		'CONN_MAX_AGE': 3600,
		'OPTIONS': {'charset': 'utf8mb4'},
	},
	'dnguyen_db.slave': {
		'NAME': 'dnguyen_api',
		'ENGINE': 'django.db.backends.mysql',
		'HOST': '172.17.0.2',
		'PORT': '3306',
		'USER': 'root',
		'PASSWORD': 'dnguyen_api_mysql3306123456',
		'CONN_MAX_AGE': 3600,
		'OPTIONS': {'charset': 'utf8mb4'},
	},
	'cooky_sql_db.master': {
		'NAME': 'CookyDemo',
		'ENGINE': 'sql_server.pyodbc',
		'HOST': 'demo.cooky.vn,1433',
		'USER': 'bepngon',
		'PASSWORD': 'C00kyDemO!@#',
		'CONN_MAX_AGE': 3600,
		'OPTIONS': {
			'driver': 'ODBC Driver 17 for SQL Server',
		},
	},
	'cooky_sql_db.slave': {
		'NAME': 'CookyDemo',
		'ENGINE': 'sql_server.pyodbc',
		'HOST': 'demo.cooky.vn,1433',
		'USER': 'bepngon',
		'PASSWORD': 'C00kyDemO!@#',
		'CONN_MAX_AGE': 3600,
		'OPTIONS': {
			'driver': 'ODBC Driver 17 for SQL Server',
		},
	},
}

MEDIA_CONFIG = {
	"upload_url": "",
	"download_url": "",
	"access_key": "",
}

NOTIFY_CONFIG = {
	"url": "",
}

VALID_IMAGE_TYPE = ["jpg", "jpeg", "png", "gif"]

CORS_ORIGIN_WHITELIST = (
)

CORS_ALLOW_HEADERS = (
	'x-cooky-api-version',
	'x-cooky-client-id',
	'x-cooky-app-type',
	'x-cooky-client-version',
	'x-cooky-access-token',
	'x-cooky-user-token',
	'x-cooky-client-language',
	'x-cooky-client-type',
	'x-cooky-timestamp',
	'x-cooky-client-referrer'
)

AWS_SNS_CONFIG = {
	'ACCESS_KEY': '',
	'SECRET_KEY': '',
	'REGION': 'ap-southeast-1'
}

AWS_SQS_CONFIG = {
	'ACCESS_KEY': '',
	'SECRET_KEY': '',
	'REGION': '',
	'EMAIL_BOUNCED_QUEUE': ''
}

GOOGLE_API_KEYS = {
	'PLACE_API_KEY': '',
	'ROUTE_API_KEY': '',
	'TIMEOUT': 10,
	'CHUNK_SIZE': 20480
}

SOCIAL_APP_ID = {
	'FACEBOOK_APP_ID': [
		''
	],
	'GOOGLE_CLIENT_ID': [
		# ------------------------------------------------------------------------
		# ANDROID
		# ------------------------------------------------------------------------
		'',
		# ------------------------------------------------------------------------
		# IOS
		# ------------------------------------------------------------------------
		'',
		# ------------------------------------------------------------------------
		# WEB
		# ------------------------------------------------------------------------
		'',
	]
}

FB_CONFIG = {
	'APP_ID': '',
	'APP_SECRET': '',
	'GRAPH_ENDPOINT': ''
}

HASHID_CONFIG = {
	"SALT": "",
	"VARIANT_DATA": 1		# must be number
}

LOCALE_CONFIG = {
	'vi': {
		'locale': 'vi_VN',
		'url': 'https://media.cooky.vn/traduora/product/vi_vn.json',
	},
	'en': {
		'locale': 'en_US',
		'url': 'https://media.cooky.vn/traduora/product/en_us.json',
	},
}

#TODO: replaced by cooky info
FAKTORY_CONNECTION = 'tcp://admin:Lucky2020!@faktory.demo.cooky.com.vn:7419'
FAKTORY_WORKER_CONFIG = {
	"default": {
		'faktory': FAKTORY_CONNECTION,
		'queues': ['default'],
		'concurrency': 2,
		'use_threads': True
	},
	"send_email": {
		'faktory': FAKTORY_CONNECTION,
		'queues': ['email_queue'],
		'concurrency': 2,
		'use_threads': True
	},
	"push_notification": {
		'faktory': FAKTORY_CONNECTION,
		'queues': ['notification_queue'],
		'concurrency': 2,
		#'log': logger.log,
		'use_threads': True
	},
	"sync_media": {
		'faktory': FAKTORY_CONNECTION,
		'queues': ['sync_media_queue'],
		'concurrency': 20,
		'use_threads': True
	},
}

APPLE_CONNECT_API = {
	'ALGORITHM': 'ES256',
	'APP_STORE_KEY_ID': 'SKCF6FV655',
	'ISSUER_ID': '69a6de91-607d-47e3-e053-5b8c7c11a4d1',
	'STORE_AUTH_KEY': '/data/release/keys/ios/AuthKey_SKCF6FV655.p8',
	'VENDOR_NUMBER': '87952446',
	'BASE_URL': 'https://api.appstoreconnect.apple.com/v1/salesReports?filter[version]=1_0&filter[vendorNumber]=87952446&filter[frequency]=DAILY&filter[reportSubType]=SUMMARY&filter[reportType]=SALES&filter[reportDate]=',
	'MAX_REQUESTS_PER_CRON_TASK': 10
}

ANDROID_GOOGLE_CLOUD_STORAGE_API = {
	'SCOPES': 'https://www.googleapis.com/auth/devstorage.read_only',
	'SERVICE_ACCOUNT_FILE': '/data/release/keys/android/cooky-vn-d1f730ae317b.json',
	'BASE_URL': 'stats/installs/installs_vn.cooky.cooky_',
	'BUCKET_NAME': 'pubsite_prod_rev_09040012874383958135'
}

SEND_BIRD_CONFIG = {
	'URL': '', #TODO: replace by cooky
	'API_TOKEN': '',
	'VERSION': 'v3',
	'TIMEOUT': 10
}

STORAGE_CLOUD = {
	# 'VNG': {
	# 	'username': '',
	# 	'password': '',
	# 	'authentication_url': '',
	# 	'project_id': '',
	# 	'container': '',
	# 	'local_path_prefix': '',
	# 	'max_retry': 2,
	# }
}

AUTH_SERVICE = {
	'host': "https://test-auth-api.cooky.com.vn",
	'app_id': 3000,  #provided by auth-api (service authorization)
	'timeout': 5,
	'retry': 3
}

def init_prometheus_data_dir(app_name=None):
	import os
	if not app_name:
		app_name = ""
	data_dir = METRICS_DATA_LOCATION % app_name
	print('day ne=' + data_dir)
	if not os.path.exists(data_dir):
		os.umask(0)
		os.makedirs(data_dir, mode=0o777)
	os.environ["prometheus_multiproc_dir"] = data_dir
	return data_dir
