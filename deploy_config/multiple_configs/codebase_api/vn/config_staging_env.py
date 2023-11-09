from codebase_lib.constants import RunningEnvironment, ServiceType
import os

RUNNING_ENVIRONMENT = RunningEnvironment.STAGING
DEBUG = False
TESTING = True

COUNTRY = 'VN'
LANGUAGE = 'en'
# GEOIP_PATH = "/opt/ip2location/ip-country.bin"

ALLOWED_HOSTS = ['*']

solr_host = 'solr.metrip.vn:8983'
if os.environ.get('SOLR_HOST'):
	solr_host = os.environ.get('SOLR_HOST')

SOLR_ENDPOINT = {
	'url': 'http://%s/solr/place' % solr_host
}

SOLR_ENDPOINT_PLAN = {
	'url': 'http://%s/solr/plan' % solr_host
}

SENTRY_DSN = ""

METRICS_DATA_LOCATION = "/data/prometheus/%s"
METRICS_IP_WHITELIST = (
	'127.0.0.1',
	'125.212.248.83',
	'14.161.17.124',
	'125.212.244.45',
	'210.211.116.165',  # metrip open vpn
)

META_FILE_URL = "https://stage-appapi.metrip.vn/meta/metadata_%s.json"
META_LOCATION = "/metadata_%s.json"
SITEMAP_LOCATION = "sitemap.xml"
META_FTP_CONFIG = {
	'host': '125.212.244.36',
	'port': 21,
	'user': 'meta_ftp_user',
	'password': 'NaMoPizzaAra2019!5',
	'timeout': 30
}

CACHE_SERVERS = {
	"default": {
		"type": "redis",
		"host": "103.147.186.46",
		"port": 6379,
		"default_timeout": 604800,
		'key_prefix': 'codebase_stage.'
	},
}

DATABASE_BACKEND = "django"
DATABASES = {
	'default': {
		'NAME': 'metrip',
		'ENGINE': 'django.db.backends.mysql',
		'HOST': '210.211.122.53',
		'PORT': '3306',
		'USER': 'metrip_live_user',
		'PASSWORD': 'Pakour2018!Yes20',
		'CONN_MAX_AGE': 3600,
		'OPTIONS': {'charset': 'utf8mb4'},
	},
	'metrip_db.slave': {
		'NAME': 'metrip',
		'ENGINE': 'django.db.backends.mysql',
		'HOST': '210.211.122.53',
		'PORT': '3306',
		'USER': 'metrip_live_user',
		'PASSWORD': 'Pakour2018!Yes20',
		'CONN_MAX_AGE': 3600,
		'OPTIONS': {'charset': 'utf8mb4'},
	},
	'metrip_db.master': {
		'NAME': 'metrip',
		'ENGINE': 'django.db.backends.mysql',
		'HOST': '210.211.122.53',
		'PORT': '3306',
		'USER': 'metrip_live_user',
		'PASSWORD': 'Pakour2018!Yes20',
		'CONN_MAX_AGE': 3600,
		'OPTIONS': {'charset': 'utf8mb4'},
	},
	'metrip_ext_db.slave': {
		'NAME': 'metrip_extension',
		'ENGINE': 'django.db.backends.mysql',
		'HOST': '210.211.122.53',
		'PORT': '3306',
		'USER': 'metrip_live_user',
		'PASSWORD': 'Pakour2018!Yes20',
		'CONN_MAX_AGE': 3600,
		'OPTIONS': {'charset': 'utf8mb4'},
	},
	'metrip_ext_db.master': {
		'NAME': 'metrip_extension',
		'ENGINE': 'django.db.backends.mysql',
		'HOST': '210.211.122.53',
		'PORT': '3306',
		'USER': 'metrip_live_user',
		'PASSWORD': 'Pakour2018!Yes20',
		'CONN_MAX_AGE': 3600,
		'OPTIONS': {'charset': 'utf8mb4'},
	},
	'metrip_tracking_db.slave': {
		'NAME': 'metrip_tracking',
		'ENGINE': 'django.db.backends.mysql',
		'HOST': '210.211.122.53',
		'PORT': '3306',
		'USER': 'metrip_live_user',
		'PASSWORD': 'Pakour2018!Yes20',
		'CONN_MAX_AGE': 3600,
		'OPTIONS': {'charset': 'utf8mb4'},
	},
	'metrip_tracking_db.master': {
		'NAME': 'metrip_tracking',
		'ENGINE': 'django.db.backends.mysql',
		'HOST': '210.211.122.53',
		'PORT': '3306',
		'USER': 'metrip_live_user',
		'PASSWORD': 'Pakour2018!Yes20',
		'CONN_MAX_AGE': 3600,
		'OPTIONS': {'charset': 'utf8mb4'},
	},
	# 'Foody.slave': {
	# 	'NAME': 'Foody',
	# 	'ENGINE': 'sql_server.pyodbc',
	# 	'HOST': '137.59.118.104,1433',
	# 	'USER': 'foody_api',
	# 	'PASSWORD': 'QhzrukN7p9IcyN7xpxCGT1oRfAyHHl8TpcSvy7/7e8M=',
	# 	'CONN_MAX_AGE': 100000,
	# 	'OPTIONS': {
	# 		'host_is_server': True,
	# 		'extra_params': 'tds_version=8.0',
	# 		'MARS_Connection': True,
	# 	},
	# },
	# 'Foody.master': {
	# 	'NAME': 'Foody',
	# 	'ENGINE': 'sql_server.pyodbc',
	# 	'HOST': '137.59.118.104,1433',
	# 	'USER': 'foody_api',
	# 	'PASSWORD': 'QhzrukN7p9IcyN7xpxCGT1oRfAyHHl8TpcSvy7/7e8M=',
	# 	'CONN_MAX_AGE': 100000,
	# 	'OPTIONS': {
	# 		'host_is_server': True,
	# 		'extra_params': 'tds_version=8.0',
	# 		'MARS_Connection': True,
	# 	},
	# },
	# 'tripnow_db.slave': {
	# 	'NAME': 'TripNow',
	# 	'ENGINE': 'sql_server.pyodbc',
	# 	'HOST': '125.212.248.57,1433',
	# 	'USER': 'tripnow',
	# 	'PASSWORD': 'iTd^56%$haG5a471a9Hyu%',
	# 	'CONN_MAX_AGE': 100000,
	# 	'OPTIONS': {
	# 		'host_is_server': True,
	# 		'extra_params': 'tds_version=8.0',
	# 		'MARS_Connection': True,
	# 	},
	# },
	# 'tripnow_db.master': {
	# 	'NAME': 'TripNow',
	# 	'ENGINE': 'sql_server.pyodbc',
	# 	'HOST': '125.212.248.57,1433',
	# 	'USER': 'tripnow',
	# 	'PASSWORD': 'iTd^56%$haG5a471a9Hyu%',
	# 	'CONN_MAX_AGE': 100000,
	# 	'OPTIONS': {
	# 		'host_is_server': True,
	# 		'extra_params': 'tds_version=8.0',
	# 		'MARS_Connection': True,
	# 	},
	# },
}

MEDIA_CONFIG = {
	"upload_url": "https://stage-media.metrip.vn/",
	"download_url": "https://stage-media.metrip.vn/",
	"access_key": "4865b700efd0291b4afad89f830bcb9a",
}

NOTIFY_CONFIG = {
	"url": "https://stage-notifyapi.metrip.vn",
}

VALID_IMAGE_TYPE = ["jpeg", "jpg", "png", "gif"]

CORS_ORIGIN_WHITELIST = (
	'https://www.metrip.vn',
	'https://stage-web.metrip.vn'
)

CORS_ALLOW_HEADERS = (
	'x-metrip-api-version',
	'x-metrip-client-id',
	'x-metrip-app-type',
	'x-metrip-client-version',
	'x-metrip-access-token',
	'x-metrip-user-token',
	'x-metrip-client-language',
	'x-metrip-client-type',
	'x-metrip-timestamp',
	'x-metrip-client-referrer'
)

AWS_SNS_CONFIG = {
	'ACCESS_KEY': 'AKIAJXPCNZN7DERUALMA',
	'SECRET_KEY': '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',
	'REGION': 'ap-southeast-1'
}

AWS_SQS_CONFIG = {
	'ACCESS_KEY': '',
	'SECRET_KEY': '',
	'REGION': '',
	'EMAIL_BOUNCED_QUEUE': ''
}

GOOGLE_API_KEYS = {
	'PLACE_API_KEY': 'AIzaSyBbLhFrKZZBOhVaWfn3cx1bPnhiTBgWNxg',
	'ROUTE_API_KEY': 'AIzaSyCUIhf5vsxU_xk9bpJ8wOMLiIjLBp5ub4I',
	'TIMEOUT': 10,
	'CHUNK_SIZE': 20480
}

SOCIAL_APP_ID = {
	'FACEBOOK_APP_ID': [
		'1928634254100301'
	],
	'GOOGLE_CLIENT_ID': [
		# ------------------------------------------------------------------------
		# ANDROID
		# ------------------------------------------------------------------------
		'407560734336-naeu0bb7q5cik1040o3bjpvhcnghj7ai.apps.googleusercontent.com',
		'407560734336-f7ld7v1n9ge2lqhl5cghjcehf8cpp376.apps.googleusercontent.com',
		'407560734336-tj4ede0terqk3mkogvlakph3r7013s9f.apps.googleusercontent.com',
		'407560734336-vl9glujee8plephmq5pe490vei50ss6s.apps.googleusercontent.com',
		# ------------------------------------------------------------------------
		# IOS
		# ------------------------------------------------------------------------
		'407560734336-24u3rfurhvm4o21tt5rghj12id2mv0ok.apps.googleusercontent.com',
		'407560734336-v9vf9jhpdlr5vt2in7ul7tgnnclqqnt4.apps.googleusercontent.com',  # old
		# ------------------------------------------------------------------------
		# WEB
		# ------------------------------------------------------------------------
		'407560734336-l0sj369iq92r7fchsa5i1ggr18gul3iv.apps.googleusercontent.com',
		'407560734336-1d52bmvo8mgr5121rf13864nfl94n133.apps.googleusercontent.com',
		'407560734336-s4865hrqg9lkl0edd2n0ihiie8rd0tu5.apps.googleusercontent.com',
		'407560734336-81ncrnsnlp2l71r8ej78eqflhvj5o6u5.apps.googleusercontent.com',
	]
}

PRERENDER_CONFIG = {
	'HOST': 'http://210.211.122.98:3003',
	'TIMEOUT': 20
}

FB_CONFIG = {
	'APP_ID': '1928634254100301',
	'APP_SECRET': '45bf12927feeb0638a5b0b7d317ceb0b',
	'GRAPH_ENDPOINT': 'https://graph.facebook.com/v3.2'
}

HASHID_CONFIG = {
	"SALT": "56cg23038gffc1749b6c1c8e428dfc1c",
	"VARIANT_DATA": 1  # must be number
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

FAKTORY_CONNECTION = 'tcp://admin:Lukaku2019!@faktory.live.metrip.vn:7419'
FAKTORY_WORKER_CONFIG = {
	"default": {
		'faktory': FAKTORY_CONNECTION,
		'queues': ['default'],
		'concurrency': 1,
		'use_threads': True
	},
	"send_email": {
		'faktory': FAKTORY_CONNECTION,
		'queues': ['email_queue'],
		'concurrency': 1,
		'use_threads': True
	},
	"push_notification": {
		'faktory': FAKTORY_CONNECTION,
		'queues': ['notification_queue'],
		'concurrency': 1,
		# 'log': logger.log,
		'use_threads': True
	}
}

APPLE_CONNECT_API = {
	'ALGORITHM': 'ES256',
	'APP_STORE_KEY_ID': '6AVZ67F4CB',
	'ISSUER_ID': '0c7dbf0d-e85d-4f8d-b584-ed15b228b80e',
	'STORE_AUTH_KEY': '/data/release/keys/apple/AuthKey_6AVZ67F4CB.p8',
	'BASE_URL': 'https://api.appstoreconnect.apple.com/v1/salesReports?filter[vendorNumber]=88019934&filter[frequency]=DAILY&filter[reportSubType]=SUMMARY&filter[reportType]=SALES&filter[reportDate]=',
	'MAX_REQUESTS_PER_CRON_TASK': 10
}

ANDROID_GOOGLE_CLOUD_STORAGE_API = {
	'SCOPES': 'https://www.googleapis.com/auth/devstorage.read_only',
	'SERVICE_ACCOUNT_FILE': '/data/release/keys/android/metrip-1533718386125-b47016c20f0e.json',
	'BASE_URL': 'stats/installs/installs_com.billandbros.metrip_',
	'BUCKET_NAME': 'pubsite_prod_rev_09996724737912625820'
}

SEND_BIRD_CONFIG = {
	'URL': 'https://api-A408D9C8-E60E-4E90-BB8E-1BE7FDF3C7E4.sendbird.com',
	'API_TOKEN': 'e96728bdcbfaa4d81cd1b7b1b45c2d3d1ac39486',
	'VERSION': 'v3',
	'TIMEOUT': 10
}

AUTH_SERVICE = {
	'host': "https://stage-auth-api.cooky.com.vn",
	'app_id': 3000,  #provided by auth-api (service authorization)
	'timeout': 5,
	'retry': 3
}

def init_prometheus_data_dir(app_name=None):
	import os
	if not app_name:
		app_name = ""
	data_dir = METRICS_DATA_LOCATION % app_name

	if not os.path.exists(data_dir):
		os.makedirs(data_dir)
	os.environ["prometheus_multiproc_dir"] = data_dir
	return data_dir
