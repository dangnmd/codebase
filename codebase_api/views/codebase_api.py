# coding=utf-8
from common.utils import parse_params, log_request
from codebase_lib.managers.models import *
from common.preprocessor import api_response_error_params, api_response_data
from .form_schema import *
from codebase_lib.managers import localization_manager


# TODO: write new or clone from metrip

@log_request(header_prefix='HTTP_X')
@parse_params(form=EmptyTypeSchema, method='GET', data_format='FORM', error_handler=api_response_error_params)
def test(request, data):
	# return api_response_data(Result.SUCCESS,
	# 	                         {'locale_test': 'test_locale_value', 'mssql_user':
	# 		                         'abc', 'test': '123'})
	# user = CookySQLDB.Customer.objects.filter(id=123).first()
	test = DnguyenDB.D_User.objects.first()
	test_locale_value = localization_manager.get_locale('test_key')
	return api_response_data(Result.SUCCESS, {'locale_test': test_locale_value,
	                                          'test': {'id': test.id, 'name': test.name}})
