# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: IMUser.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='IMUser.proto',
  package='PBData.IM',
  serialized_pb=_b('\n\x0cIMUser.proto\x12\tPBData.IM\"F\n\x08UserInfo\x12\x0b\n\x03uid\x18\x01 \x02(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0c\n\x04icon\x18\x03 \x01(\r\x12\x11\n\tsignature\x18\x04 \x01(\t\"\xa4\x01\n\nUserOption\x12\x0b\n\x03uid\x18\x01 \x02(\r\x12\x12\n\x07option1\x18\x02 \x01(\x05:\x01\x32\x12\x0f\n\x07option2\x18\x03 \x01(\x05\x12\x0f\n\x07option3\x18\x04 \x01(\x05\x12\x0f\n\x07option4\x18\x05 \x01(\x05\x12\x0f\n\x07option5\x18\x06 \x01(\x05\x12\x0f\n\x07option6\x18\x07 \x01(\x05\x12\x0f\n\x07option7\x18\x08 \x01(\x05\x12\x0f\n\x07option8\x18\t \x01(\x05\"\x86\x01\n\tUserLimit\x12\x0b\n\x03uid\x18\x01 \x02(\r\x12\x0c\n\x04type\x18\x02 \x02(\r\x12\r\n\x05\x63ount\x18\x03 \x02(\r\x12\r\n\x05start\x18\x04 \x02(\r\"@\n\x04Type\x12\x18\n\x14LIMIT_ADD_TEMP_BUDDY\x10\x01\x12\x1e\n\x1aLIMIT_SEARCH_USER_BY_EMAIL\x10\x02')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_USERLIMIT_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='PBData.IM.UserLimit.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='LIMIT_ADD_TEMP_BUDDY', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LIMIT_SEARCH_USER_BY_EMAIL', index=1, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=337,
  serialized_end=401,
)
_sym_db.RegisterEnumDescriptor(_USERLIMIT_TYPE)


_USERINFO = _descriptor.Descriptor(
  name='UserInfo',
  full_name='PBData.IM.UserInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='PBData.IM.UserInfo.uid', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='PBData.IM.UserInfo.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='icon', full_name='PBData.IM.UserInfo.icon', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='signature', full_name='PBData.IM.UserInfo.signature', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=27,
  serialized_end=97,
)


_USEROPTION = _descriptor.Descriptor(
  name='UserOption',
  full_name='PBData.IM.UserOption',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='PBData.IM.UserOption.uid', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='option1', full_name='PBData.IM.UserOption.option1', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=2,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='option2', full_name='PBData.IM.UserOption.option2', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='option3', full_name='PBData.IM.UserOption.option3', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='option4', full_name='PBData.IM.UserOption.option4', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='option5', full_name='PBData.IM.UserOption.option5', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='option6', full_name='PBData.IM.UserOption.option6', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='option7', full_name='PBData.IM.UserOption.option7', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='option8', full_name='PBData.IM.UserOption.option8', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=100,
  serialized_end=264,
)


_USERLIMIT = _descriptor.Descriptor(
  name='UserLimit',
  full_name='PBData.IM.UserLimit',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='PBData.IM.UserLimit.uid', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='type', full_name='PBData.IM.UserLimit.type', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='count', full_name='PBData.IM.UserLimit.count', index=2,
      number=3, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='start', full_name='PBData.IM.UserLimit.start', index=3,
      number=4, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _USERLIMIT_TYPE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=267,
  serialized_end=401,
)

_USERLIMIT_TYPE.containing_type = _USERLIMIT
DESCRIPTOR.message_types_by_name['UserInfo'] = _USERINFO
DESCRIPTOR.message_types_by_name['UserOption'] = _USEROPTION
DESCRIPTOR.message_types_by_name['UserLimit'] = _USERLIMIT

UserInfo = _reflection.GeneratedProtocolMessageType('UserInfo', (_message.Message,), dict(
  DESCRIPTOR = _USERINFO,
  __module__ = 'IMUser_pb2'
  # @@protoc_insertion_point(class_scope:PBData.IM.UserInfo)
  ))
_sym_db.RegisterMessage(UserInfo)

UserOption = _reflection.GeneratedProtocolMessageType('UserOption', (_message.Message,), dict(
  DESCRIPTOR = _USEROPTION,
  __module__ = 'IMUser_pb2'
  # @@protoc_insertion_point(class_scope:PBData.IM.UserOption)
  ))
_sym_db.RegisterMessage(UserOption)

UserLimit = _reflection.GeneratedProtocolMessageType('UserLimit', (_message.Message,), dict(
  DESCRIPTOR = _USERLIMIT,
  __module__ = 'IMUser_pb2'
  # @@protoc_insertion_point(class_scope:PBData.IM.UserLimit)
  ))
_sym_db.RegisterMessage(UserLimit)


# @@protoc_insertion_point(module_scope)