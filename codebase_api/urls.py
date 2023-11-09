from django.conf.urls import url
from common.prometheus_utils import ExtendedMetricsMiddleware
from .views import codebase_api, swagger
from codebase_lib import monitoring

urlpatterns = [
	url(r'^metrics$', ExtendedMetricsMiddleware.metrics_snapshot),
	url(r'^api/health$', monitoring.check_health, {'api': 'codebase_api'}),
	url(r'^s2s/refresh_locales$', monitoring.refresh_locales),
	url(r'^api/swagger$', swagger.api_index),

	url(r'^s2s/test$', codebase_api.test),
	url(r'^s2s/swagger$', swagger.s2s_index),
]
