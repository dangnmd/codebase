from codebase_lib import config, constants

DEBUG = config.DEBUG
TEST = config.TESTING

LOGGER_CONFIG = {
	'log_dir': './log/',
	'sentry_dsn': config.SENTRY_DSN,
	'environment': constants.RunningEnvironment.get_name(config.RUNNING_ENVIRONMENT)
}

INSTALLED_APPS = (
	'raven.contrib.django.raven_compat',
	'codebase_lib'
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'raven.contrib.django.middleware.SentryLogMiddleware',
)

# config.CACHE_SERVERS = {
# 	'default':  {
# 		'type': 'memory',
# 		'default_timeout': 60,
# 		'trim_interval': 60
# 	}
# }

# TODO: update for cooky
SECRET_KEY = "+#58uhajc*r@kjlmxqq5vcs9#kztb1x7e^#s2orllq9@mvuhmb"

ROOT_URLCONF = 'cron_service.urls'
DATABASE_BACKEND = 'django'
DATABASES = config.DATABASES
DATABASE_ROUTERS = ['common.django_model.DatabaseRouter',]
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_TZ = False


CRON_PERIOD_SETTINGS = {
	"PUSH_TO_ENDPOINT": "*/10 * * * * *",
	"APPLE_INSTALL_COUNT": "*/5 * * * * *",
	"ANDROID_INSTALL_COUNT": "*/5 * * * * *",
}

