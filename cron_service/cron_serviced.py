import os
import sys
from django.core.wsgi import get_wsgi_application

curr_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(curr_dir)
sys.path.append(os.path.join(curr_dir, '../'))

from cron_service import settings
from common import context
context.init_django('.', 'settings')

application = get_wsgi_application()

from common import crontask
from cron_service.services.get_ios_install_count_task import get_ios_install_count_task
from cron_service.services.get_android_install_count_task import get_android_install_count_task

if __name__ == "__main__":
	def main():
        #crontask.register_task(settings.CRON_PERIOD_SETTINGS["APPLE_INSTALL_COUNT"], task=get_ios_install_count_task)
        #crontask.register_task(settings.CRON_PERIOD_SETTINGS["ANDROID_INSTALL_COUNT"], task=get_android_install_count_task)
		crontask.run()

	from common.daemon import Daemon
	Daemon(main, os.path.abspath(__file__).replace(".py", ".pid"), "./log/daemon.log").main()
