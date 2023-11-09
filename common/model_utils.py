#!!!Deprecated, use django_model instead
# pylint: skip-file

from .django_model import *

KeepAliveQuerySet = AdvancedQuerySet
KeepAliveManager = AdvancedManager

from django.db import models
from django.db.models.query import QuerySet
from datetime import datetime
from . import crypt

def get_sharding_model(model, kwargs):
	if 'shard' in kwargs:
		shard = kwargs.pop('shard')
	elif 'sharding_key' in kwargs and getattr(model, 'sharding_func', None):
		shard = model.sharding_func(kwargs.pop('sharding_key'))
	else:
		raise Exception('no shard specified')

	class Meta:
		db_table = model._meta.db_table % shard
	new_model = type('%s_%s' % (model.__name__, shard), model.__bases__[1:], {
		'__module__': model.__module__, 'Meta': Meta, 'shard': True, 'objects': models.Manager()
	})
	return new_model

class ShardingQuerySet(QuerySet):
	def filter(self, *args, **kwargs):
		return get_sharding_model(self.model, kwargs).objects.using(self._db).filter(*args, **kwargs)
	def get(self, *args, **kwargs):
		return get_sharding_model(self.model, kwargs).objects.using(self._db).get(*args, **kwargs)
	def update(self, **kwargs):
		return get_sharding_model(self.model, kwargs).objects.using(self._db).update(**kwargs)
	def create(self, **kwargs):
		return get_sharding_model(self.model, kwargs).objects.using(self._db).create(**kwargs)

class ShardingManager(models.Manager):
	def get_query_set(self):
		return ShardingQuerySet(self.model, using=self._db)

class ShardingMixin(object):
	@staticmethod
	def __new__(cls, *args, **kwargs):
		return get_sharding_model(cls, kwargs)(*args, **kwargs)

# Common Sharding Functions:
def shard_by_datetime(format):
	def func(timestamp):
		return datetime.fromtimestamp(int(timestamp)).strftime(format)
	return staticmethod(func)
def shard_by_crchash(base):
	def func(s):
		return crypt.crc32(s) % base
	return staticmethod(func)
def shard_by_mod(base):
	def func(n):
		return n % base
	return staticmethod(func)
