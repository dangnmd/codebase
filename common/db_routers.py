#Deprecated

from django.conf import settings

class DatabaseRouter(object):
	# pylint: disable=protected-access
	def db_for_read(self, model, **hints):
		# Point all read operations to the specific database.
		if hasattr(model, 'read_db_connection'):
			return model.read_db_connection
		if model._meta.app_label in settings.DATABASE_APPS_MAPPING:
			return settings.DATABASE_APPS_MAPPING[model._meta.app_label]
		return 'default'

	def db_for_write(self, model, **hints):
		# Point all write operations to the specific database.
		if hasattr(model, 'write_db_connection'):
			return model.write_db_connection
		if model._meta.app_label in settings.DATABASE_APPS_MAPPING:
			return settings.DATABASE_APPS_MAPPING[model._meta.app_label]
		return 'default'
