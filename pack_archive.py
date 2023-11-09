import zipfile
import os
import sys
import shutil

def copytree(src, dst, symlinks=False, ignore=None):
	for item in os.listdir(src):
		s = os.path.join(src, item)
		d = os.path.join(dst, item)
		if os.path.isdir(s):
			shutil.copytree(s, d, symlinks, ignore)
		else:
			shutil.copy2(s, d)

def filter_file(filename):
	if filename.endswith('.zip'):
		return False
	if filename.endswith('.pyc'):
		return False
	if filename.endswith('.lib'):
		return False
	if '.log' in filename:
		return False
	if filename.startswith('.') and not filename.endswith('.gitkeep') and not filename.endswith('.env'):
		return False
	return True

ignore_folders = ['deploy_config', 'monitoring']
app_folders = ['codebase_api', 'cron_service']
def filter_folder(dirpath, deploy_server_type):
	for dirname in dirpath.split(os.path.sep):
		if (len(dirname) > 1 and dirname.startswith('.')):
			return False
		if "deployment_config" in dirname:
			return False
		if dirname in app_folders and not dirname.endswith(deploy_server_type):
			return False
		if dirname in ignore_folders:
			return False
	return True


if __name__ == "__main__":
	env_type = "test_env"
	deploy_app_type = "auth_api"
	deploy_server_port = "8000"
	country = "vn"
	if len(sys.argv) >= 2:
		if sys.argv[1] in ["live_env", "staging_env", "test_env"]:
			env_type = sys.argv[1]
	if len(sys.argv) >= 3:
		if sys.argv[2] in app_folders:
			deploy_app_type = sys.argv[2]
	if len(sys.argv) >= 4:
		country = sys.argv[3]
	if len(sys.argv) >= 5:
		deploy_server_port = sys.argv[4]

	#prepare deploy config
	CURRENT_DIR = os.getcwd()
	#DEPLOY_DIR = os.path.join(CURRENT_DIR, "deploy")
	DEPLOY_COMMON_DIR = os.path.join(CURRENT_DIR, "common", "deploy")
	DEPLOY_CONFIG_DIR = os.path.join(CURRENT_DIR, "deploy_config",)
	#SCRIPTS_DIR = os.path.join(DEPLOY_CONFIG_DIR, "scripts")
	SETTINGS_COUNTRY_DIR = os.path.join(DEPLOY_CONFIG_DIR, "multiple_configs", deploy_app_type, country)
	CONFIG_FILE_DIR = os.path.join(CURRENT_DIR, "codebase_lib", "config.py")
	TEST_CONSTANT_FILE_DIR = os.path.join(CURRENT_DIR, "test", "test_constants.py")

	# update config file
	shutil.copy(os.path.join(SETTINGS_COUNTRY_DIR, "config_%s.py" % env_type), CONFIG_FILE_DIR)
	shutil.copy(os.path.join(SETTINGS_COUNTRY_DIR, "test_constants.py"), TEST_CONSTANT_FILE_DIR)

	# copy deploy.sh
	shutil.copy(os.path.join(DEPLOY_COMMON_DIR, "deploy.sh"), CURRENT_DIR)
	# copy docker .env
	shutil.copy(os.path.join(DEPLOY_CONFIG_DIR, env_type, deploy_app_type, ".env"), CURRENT_DIR)

	ARCHIVE_PREFIX = deploy_app_type + '_' + deploy_server_port + '_' + env_type
	ARCHIVE_NAME = ARCHIVE_PREFIX + '.zip'

	print(('Packing', ARCHIVE_NAME))
	f = zipfile.ZipFile(ARCHIVE_NAME, 'w', zipfile.ZIP_DEFLATED)
	for dirpath, dirnames, filenames in os.walk('.'):
		for filename in filenames:
			fullpath = os.path.join(dirpath, filename)
			if filter_folder(dirpath, deploy_app_type):
				if filter_file(filename):
					f.write(fullpath, os.path.join(ARCHIVE_PREFIX, fullpath))
	f.close()
	print('Pack complete')

	# reset config file
	with open(CONFIG_FILE_DIR, 'w') as file:
		file.write("from deploy_config.configs.vn.config_dev_env import *")

	with open(TEST_CONSTANT_FILE_DIR, 'w') as file:
		file.write("from deploy_config.configs.vn.test_constants import *")

	#shutil.rmtree(DEPLOY_DIR, ignore_errors=True)
