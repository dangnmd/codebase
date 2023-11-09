from django.db.models.sql.query import Query
from django.db.models.query import QuerySet

def _query_add_force_index(self, index_name):
	self.force_index = index_name

_original_query_clone = Query.clone

def _new_query_clone(self, *args, **kwargs):
	clone_obj = _original_query_clone(self, *args, **kwargs)
	if clone_obj and self.force_index:
		clone_obj.force_index = self.force_index
	return clone_obj

def _queryset_force_index(self, index_name):
	assert isinstance(index_name, str), "index_name is not str: type=%s" % type(index_name)
	assert index_name, "index_name is empty"
	obj = self._clone()
	if obj._sticky_filter:
		obj.query.filter_is_sticky = True
		obj._sticky_filter = False
	obj.query.add_force_index(index_name)
	return obj

def patch_mssql_compiler():
	return

def patch_mysql_compiler():
	from django.db.backends.mysql import compiler

	class SQLCompiler(compiler.SQLCompiler):
		def get_from_clause(self):
			result, params = super(SQLCompiler, self).get_from_clause()
			if self.query.force_index:
				assert (len(self.query.table_map) == 1 and not self.query.extra_tables), "only support force_index for query with 1 table"
				result.append('FORCE INDEX(%s)' % self.query.force_index)

			return result, params

	compiler.SQLCompiler = SQLCompiler

def apply_patch():
	setattr(Query, 'force_index', None)
	setattr(Query, 'add_force_index', _query_add_force_index)
	Query.clone = _new_query_clone
	setattr(QuerySet, 'force_index', _queryset_force_index)
	patch_mysql_compiler()

