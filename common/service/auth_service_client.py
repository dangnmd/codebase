from config import config
from common.authapiservice import AuthServiceClient

auth_api_client = None
if hasattr(config, 'AUTH_SERVICE'):
	auth_api_client = AuthServiceClient(**config.AUTH_SERVICE)


def request(api, data, method="POST", disable_retry=False):
	return auth_api_client.request(api, data, method, disable_retry)
