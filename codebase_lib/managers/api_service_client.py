import codebase_lib.config
from common.fapiservice import FApiServiceClient

api_client = None
if hasattr(codebase_lib.config, 'API_SERVICE_SERVER'):
	api_client = FApiServiceClient(**codebase_lib.config.API_SERVICE_SERVER)

def request(api, data, method="POST", disable_retry=False):
	return api_client.request(api, data, method, disable_retry)
