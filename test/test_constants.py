import os
PROJECT_NAME = os.environ.get('PROJECT_NAME')
if PROJECT_NAME == "codebase_api":
	from deploy_config.multiple_configs.codebase_api.vn.test_constants import *
