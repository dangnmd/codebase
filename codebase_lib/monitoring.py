import os

from django.http import HttpResponseForbidden, HttpResponse
from codebase_lib.utils import api_response_data
from codebase_lib.constants import Result
from codebase_lib.managers import localization_manager

def check_health(request, api):
	# ip_address = request.META.get('HTTP_X_REAL_IP')
	# if ip_address:
	# 	return HttpResponseForbidden()
	if os.path.isfile('/opt/project/health.txt'):
		return api_response_data(Result.SUCCESS, api)
	else:
		return HttpResponse(status=500)

def refresh_locales(request):
	localization_manager.init_locales()
	test_resource = localization_manager.get_locale('test')
	return api_response_data(Result.SUCCESS, {'test': test_resource})