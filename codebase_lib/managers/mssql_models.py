from datetime import datetime
import struct
import binascii
from common import dbmodel
from codebase_lib import config

db = dbmodel.get_db()
if not db:
	db = dbmodel.init_db(config.DATABASE_BACKEND, None)

class CustomTimestampField(db.Field):
	def from_db_value(self, value, expression, connection, context):
		if not value:
			return None
		return '0x' + binascii.hexlify(str(value)).upper()

class FieldsExclusion(db.Model):
	ExclusionFields = None

	class Meta:
		abstract = True

	def __init__(self, *args, **kwargs):
		if not self.ExclusionFields:
			self.ExclusionFields = [x.name for x in self._meta.get_fields() if isinstance(x, CustomTimestampField)]
		else:
			self.ExclusionFields.extend([x.name for x in self._meta.get_fields() if isinstance(x, CustomTimestampField)])
		super(FieldsExclusion, self).__init__(*args, **kwargs)

	def save(self, **kwargs):
		if self.ExclusionFields:
			excludes = tuple(self._meta.get_field(x) for x in self.ExclusionFields if hasattr(self, x))
			self._meta.local_concrete_fields = tuple(x for x in self._meta.local_concrete_fields if x not in excludes)
		super(FieldsExclusion, self).save(**kwargs)

def _convert_utf16_to_utf8(str_data):
	str_data = str_data.encode('utf-16le')
	str_data = ''.join(chr(x).encode('utf-8') for x in struct.unpack('<' + 'H' * (len(str_data) // 2), str_data))
	return str_data.decode('utf-8')

class CharUtf16Field(db.CharField):

	def __init__(self, *args, **kwargs):
		super(CharUtf16Field, self).__init__(*args, **kwargs)

	def get_prep_value(self, value):
		value = super(CharUtf16Field, self).get_prep_value(value)
		if value:
			return _convert_utf16_to_utf8(value)

		return value

class TextUtf16Field(db.TextField):

	def __init__(self, *args, **kwargs):
		super(TextUtf16Field, self).__init__(*args, **kwargs)

	def get_prep_value(self, value):
		value = super(TextUtf16Field, self).get_prep_value(value)
		if value:
			return _convert_utf16_to_utf8(value)

		return value

class CookySQLDB:
	class CookySQLDBConfig:
		class Config:
			db_for_read = 'cooky_sql_db.slave'
			db_for_write = 'cooky_sql_db.master'

	class Customer(CookySQLDBConfig, db.Model):
		id = db.AutoField(db_column='Id', primary_key=True)
		username = db.CharField(db_column='UserName', max_length=300)

		class Meta:
			managed = False
			db_table = 'Customer'
