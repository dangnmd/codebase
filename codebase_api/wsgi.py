"""
WSGI config for authentication_api project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codebase_api.settings")
from codebase_lib import config
#if config.RUNNING_ENVIRONMENT != config.RunningEnvironment.DEVELOPMENT:
#	import monkey_patches
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
app = application

#import patch_force_index
#patch_force_index.apply_patch()
from codebase_lib.managers.localization_manager import init_locales
init_locales()
