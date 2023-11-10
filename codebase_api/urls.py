from django.urls import re_path
from common.prometheus_utils import ExtendedMetricsMiddleware
from .views import codebase_api, swagger
from codebase_lib import monitoring

urlpatterns = [
	re_path(r'^metrics$', ExtendedMetricsMiddleware.metrics_snapshot),
	re_path(r'^api/health$', monitoring.check_health, {'api': 'codebase_api'}),
	re_path(r'^s2s/refresh_locales$', monitoring.refresh_locales),
	re_path(r'^api/swagger$', swagger.api_index),

	re_path(r'^s2s/test$', codebase_api.test),
	re_path(r'^s2s/swagger$', swagger.s2s_index),
]
