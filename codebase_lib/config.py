import os
PROJECT_NAME = os.environ.get('PROJECT_NAME')  # get env var from settings
print('project name ne %s', PROJECT_NAME)
#if PROJECT_NAME == "codebase_api":
#	from deploy_config.multiple_configs.codebase_api.vn.config_dev_env import *
from deploy_config.multiple_configs.codebase_api.vn.config_dev_env import *
