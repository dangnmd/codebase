import os
PROJECT_NAME = os.environ.get('PROJECT_NAME')  # get env var from settings
if PROJECT_NAME == "codebase_api":
	from deploy_config.multiple_configs.codebase_api.vn.config_dev_env import *