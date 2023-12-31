import re
from google.protobuf.descriptor import FieldDescriptor, FileDescriptor
from google.protobuf import message
from . import jsonutils
from .enum_type import EnumBase

TYPE_CALLABLE_MAP = {
	FieldDescriptor.TYPE_DOUBLE: float,
	FieldDescriptor.TYPE_FLOAT: float,
	FieldDescriptor.TYPE_INT32: int,
	FieldDescriptor.TYPE_INT64: int,
	FieldDescriptor.TYPE_UINT32: int,
	FieldDescriptor.TYPE_UINT64: int,
	FieldDescriptor.TYPE_SINT32: int,
	FieldDescriptor.TYPE_SINT64: int,
	FieldDescriptor.TYPE_FIXED32: int,
	FieldDescriptor.TYPE_FIXED64: int,
	FieldDescriptor.TYPE_SFIXED32: int,
	FieldDescriptor.TYPE_SFIXED64: int,
	FieldDescriptor.TYPE_BOOL: bool,
	FieldDescriptor.TYPE_STRING: str,
	FieldDescriptor.TYPE_BYTES: lambda b: b.encode("hex"),
	FieldDescriptor.TYPE_ENUM: int,
}

TYPE_CALLABLE_MAP_RAW = TYPE_CALLABLE_MAP.copy()
TYPE_CALLABLE_MAP_RAW[FieldDescriptor.TYPE_BYTES] = str

def repeated(type_callable):
	return lambda value_list: [type_callable(value) for value in value_list]

def enum_label_name(field, value):
	return field.enum_type.values_by_number[int(value)].name

def pb_to_dict(pb, type_callable_map=None, use_enum_labels=False, raw=False):
	if type_callable_map is None:
		if raw:
			type_callable_map = TYPE_CALLABLE_MAP_RAW
		else:
			type_callable_map = TYPE_CALLABLE_MAP
	result_dict = {}
	for field, value in pb.ListFields():
		if field.type == FieldDescriptor.TYPE_MESSAGE:
			# recursively encode protobuf sub-message
			type_callable = lambda pb: pb_to_dict(pb,
				type_callable_map=type_callable_map,
				use_enum_labels=use_enum_labels)
		elif field.type in type_callable_map:
			type_callable = type_callable_map[field.type]
		else:
			type_callable = lambda value: '!unknow_type:' + repr(value)
		if use_enum_labels and field.type == FieldDescriptor.TYPE_ENUM:
			type_callable = lambda value: enum_label_name(field, value)	# pylint: disable=cell-var-from-loop
		if field.label == FieldDescriptor.LABEL_REPEATED:
			type_callable = repeated(type_callable)
		result_dict[field.name] = type_callable(value)
	return result_dict

def pb_to_str(pb):
	return jsonutils.to_json(pb_to_dict(pb))

def is_pb_message(data):
	return isinstance(data, message.Message)

def list_all_fields(pb):
	return (i.name for i in pb.DESCRIPTOR.fields)

def set_pb_from_dict(pb, dict_instance, exclude=None):
	fields = set(dict_instance.keys())
	if exclude:
		fields = fields.difference(exclude)
	for field in fields:
		value = dict_instance[field]
		if isinstance(value, dict):
			set_pb_from_dict(getattr(pb, field), value, exclude)
		elif isinstance(value, (tuple, list, set)):
			if value:
				pb_field = getattr(pb, field)
				if isinstance(value[0], dict):
					for v in value:
						pb_field.add()
						set_pb_from_dict(pb_field[-1], v, exclude)
				else:
					pb_field.extend(value)
		else:
			setattr(pb, field, value)
	return pb

def set_repeated_from_dict_list(pb, dict_list, exclude=None):
	if not dict_list:
		return pb
	fields = set(dict_list[0].keys())
	if exclude:
		fields = fields.difference(exclude)
	for d in dict_list:
		one_pb = pb.add()
		for field in fields:
			setattr(one_pb, field, d[field])
	return pb

def set_pb_from_model(pb, model_instance, exclude=None):
	# pylint: disable=protected-access
	model_fields = model_instance._meta.get_all_field_names()
	common_fields = set(model_fields).intersection(set(list_all_fields(pb)))
	if exclude:
		common_fields = common_fields.difference(exclude)
	for i in common_fields:
		setattr(pb, i, getattr(model_instance, i))
	return pb

def set_repeated_from_model(pb, queryset, exclude=None):
	# pylint: disable=protected-access
	if not queryset:
		return pb
	model_fields = queryset[0]._meta.get_all_field_names()
	pb_fields = (i.name for i in pb._message_descriptor.fields)
	common_fields = set(model_fields).intersection(set(pb_fields))
	if exclude:
		common_fields = common_fields.difference(exclude)
	for one_model in queryset:
		one_pb = pb.add()
		for field in common_fields:
			setattr(one_pb, field, getattr(one_model, field))
	return pb

def pb_enum_values_to_class(values, name):
	fields = dict((v.name, v.number) for v in values)
	return type(name, (EnumBase,), fields)

def pb_enum_to_class(pb, name):
	""" Convert enum type in protocol buffer to python class
	:param pb: `pb` can be a protocol buffer message or module.
		If enum is defined inside message, pass the message as `pb`.
		If enum is defined in global scope in file, pass the module of the file as `pb`.
	:param name: enum type name
	:return: enum class based on `enum_type.EnumBase`
	"""
	if isinstance(pb.DESCRIPTOR, FileDescriptor):
		return pb_enum_values_to_class(getattr(pb, '_' + name.upper()).values, name)
	else:
		return pb_enum_values_to_class(pb.DESCRIPTOR.enum_types_by_name[name].values, name)


# Protobuf Validator

class _ItemValidator(object):

	def validate(self, path, value):
		if self._validate(value):
			return None
		return self._format_error(path, value)

	def _format_error(self, path, value):
		return self._error_template % (path, value)

class _RequiredValidator(_ItemValidator):

	def __init__(self, field_name):
		self._field_name = field_name
		self._error_template = 'required:%s,%s,%s'

	def _validate(self, value):
		return value.HasField(self._field_name)

	def _format_error(self, path, value):
		return self._error_template % (self._field_name, path, '')

class _MaxItemValidator(_ItemValidator):

	def __init__(self, ref):
		self._ref = ref
		self._error_template = 'maxItem:%s,%%s,%%s' % ref

	def _validate(self, value):
		return len(value) <= self._ref

	def _format_error(self, path, value):
		return self._error_template % (path, len(value))

class _MinItemValidator(_ItemValidator):

	def __init__(self, ref):
		self._ref = ref
		self._error_template = 'minItem:%s,%%s,%%s' % ref

	def _validate(self, value):
		return len(value) >= self._ref

	def _format_error(self, path, value):
		return self._error_template % (path, len(value))

class _MaximumValidator(_ItemValidator):

	def __init__(self, ref):
		self._ref = ref
		self._error_template = 'maximum:%s,%%s,%%s' % ref

	def _validate(self, value):
		return value <= self._ref

class _MinimumValidator(_ItemValidator):

	def __init__(self, ref):
		self._ref = ref
		self._error_template = 'minimum:%s,%%s,%%s' % ref

	def _validate(self, value):
		return value >= self._ref

class _LengthValidator(_ItemValidator):

	def __init__(self, ref):
		self._ref = ref
		self._error_template = 'length:%s,%%s,%%s' % ref

	def _validate(self, value):
		return len(value) == self._ref

class _MaxLengthValidator(_ItemValidator):

	def __init__(self, ref):
		self._ref = ref
		self._error_template = 'maxLength:%s,%%s,%%s' % ref

	def _validate(self, value):
		return len(value) <= self._ref

class _MinLengthValidator(_ItemValidator):

	def __init__(self, ref):
		self._ref = ref
		self._error_template = 'minLength:%s,%%s,%%s' % ref

	def _validate(self, value):
		return len(value) >= self._ref

class _PatternValidator(_ItemValidator):

	def __init__(self, pattern):
		if not pattern.endswith('$'):
			pattern += '$'
		self._pattern = re.compile(pattern)
		self._error_template = 'pattern:%s,%s,%s'

	def _validate(self, value):
		return self._pattern.match(value) is not None

	def _format_error(self, path, value):
		return self._error_template % (self._pattern.pattern, path, value)

def _create_validator(schema):
	validators = {'v': []}
	for key, value in schema.items():
		if key == 'type':
			validators['t'] = value
		elif key == 'properties':
			validators['f'] = {}
			for pname, pvalue in value.items():
				validators['f'][pname] = _create_validator(pvalue)
		elif key == 'required':
			for field_name in value:
				if schema.get('properties', {}).get(field_name, {}).get('type') != 'array':
					validators['v'].append(_RequiredValidator(field_name))
		elif key == 'items':
			validators['i'] = _create_validator(value)
		elif key == 'maxItems':
			validators['v'].append(_MaxItemValidator(value))
		elif key == 'minItems':
			validators['v'].append(_MinItemValidator(value))
		elif  key == 'maximum':
			validators['v'].append(_MaximumValidator(value))
		elif  key == 'minimum':
			validators['v'].append(_MinimumValidator(value))
		elif  key == 'length':
			validators['v'].append(_LengthValidator(value))
		elif key == 'maxLength':
			validators['v'].append(_MaxLengthValidator(value))
		elif key == 'minLength':
			validators['v'].append(_MinLengthValidator(value))
		elif key == 'pattern':
			validators['v'].append(_PatternValidator(value))
	return validators

def _validate_iter_errors(instance, validator, path='.'):
	try:
		for v in validator['v']:
			result = v.validate(path, instance)
			if result is not None:
				yield result
		if 'f' in validator:
			for fname, fvalidator in validator['f'].items():
				if fvalidator.get('t') == 'array' or instance.HasField(fname):
					fvalue = getattr(instance, fname)
					for error in _validate_iter_errors(fvalue, fvalidator, path + '/' + fname):
						yield error
		if 'i' in validator:
			ivalidator = validator['i']
			for index, fvalue in enumerate(instance):
				for error in _validate_iter_errors(fvalue, ivalidator, path + '/' + str(index)):
					yield error
	except Exception as ex:
		yield 'exception:' + str(ex)

class PBValidator(object):
	"""
	supported schema
	common: type
	object: properties, required
	array: items, maxItems, minItems
	integer: minimum, maximum
	number: minimum, maximum
	string: length, minLength, maxLength, pattern
	bytes: length, minLength, maxLength
	if array field included in required validation, please indicate its type is array
	"""

	def __init__(self, schema):
		self._schema = None
		self._validator = None
		self.schema = schema

	@property
	def schema(self):
		return self._schema

	@schema.setter
	def schema(self, schema):
		self._schema = schema
		self._validator = _create_validator(self._schema)

	def iter_errors(self, instance):
		for error in _validate_iter_errors(instance, self._validator):
			yield error

	def validate(self, instance):
		for error in self.iter_errors(instance):
			raise error

	def is_valid(self, instance):
		error = next(self.iter_errors(instance), None)
		return error is None
