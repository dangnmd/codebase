# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: LogModel.proto

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
  name='LogModel.proto',
  package='PBData',
  serialized_pb=_b('\n\x0eLogModel.proto\x12\x06PBData\"g\n\x12UserChangeUsername\x12\x0b\n\x03uid\x18\x01 \x01(\x04\x12\x10\n\x08\x66romname\x18\x02 \x01(\t\x12\x0e\n\x06toname\x18\x03 \x01(\t\x12\x0f\n\x07user_ip\x18\x04 \x01(\t\x12\x11\n\ttimestamp\x18\x05 \x01(\r\"g\n\x12UserChangePassword\x12\x0b\n\x03uid\x18\x01 \x01(\x04\x12\x10\n\x08\x66rompass\x18\x02 \x01(\t\x12\x0e\n\x06topass\x18\x03 \x01(\t\x12\x0f\n\x07user_ip\x18\x04 \x01(\t\x12\x11\n\ttimestamp\x18\x05 \x01(\r\"\x8b\x01\n\x0c\x46\x62\x43onnectLog\x12\n\n\x02id\x18\x01 \x01(\x04\x12\x0b\n\x03uid\x18\x02 \x01(\x04\x12\x0e\n\x06\x66\x62_uid\x18\x03 \x01(\x04\x12\x0e\n\x06\x61pp_id\x18\x04 \x01(\x04\x12\x0e\n\x06\x61\x63tion\x18\x05 \x01(\r\x12\x11\n\tdirection\x18\x06 \x01(\r\x12\n\n\x02ip\x18\x07 \x01(\r\x12\x13\n\x0b\x63reate_time\x18\x08 \x01(\r')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_USERCHANGEUSERNAME = _descriptor.Descriptor(
  name='UserChangeUsername',
  full_name='PBData.UserChangeUsername',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='PBData.UserChangeUsername.uid', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fromname', full_name='PBData.UserChangeUsername.fromname', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='toname', full_name='PBData.UserChangeUsername.toname', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='user_ip', full_name='PBData.UserChangeUsername.user_ip', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='PBData.UserChangeUsername.timestamp', index=4,
      number=5, type=13, cpp_type=3, label=1,
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
  serialized_start=26,
  serialized_end=129,
)


_USERCHANGEPASSWORD = _descriptor.Descriptor(
  name='UserChangePassword',
  full_name='PBData.UserChangePassword',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='PBData.UserChangePassword.uid', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frompass', full_name='PBData.UserChangePassword.frompass', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='topass', full_name='PBData.UserChangePassword.topass', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='user_ip', full_name='PBData.UserChangePassword.user_ip', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='PBData.UserChangePassword.timestamp', index=4,
      number=5, type=13, cpp_type=3, label=1,
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
  serialized_start=131,
  serialized_end=234,
)


_FBCONNECTLOG = _descriptor.Descriptor(
  name='FbConnectLog',
  full_name='PBData.FbConnectLog',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='PBData.FbConnectLog.id', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='uid', full_name='PBData.FbConnectLog.uid', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fb_uid', full_name='PBData.FbConnectLog.fb_uid', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='app_id', full_name='PBData.FbConnectLog.app_id', index=3,
      number=4, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='action', full_name='PBData.FbConnectLog.action', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='direction', full_name='PBData.FbConnectLog.direction', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ip', full_name='PBData.FbConnectLog.ip', index=6,
      number=7, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='create_time', full_name='PBData.FbConnectLog.create_time', index=7,
      number=8, type=13, cpp_type=3, label=1,
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
  serialized_start=237,
  serialized_end=376,
)

DESCRIPTOR.message_types_by_name['UserChangeUsername'] = _USERCHANGEUSERNAME
DESCRIPTOR.message_types_by_name['UserChangePassword'] = _USERCHANGEPASSWORD
DESCRIPTOR.message_types_by_name['FbConnectLog'] = _FBCONNECTLOG

UserChangeUsername = _reflection.GeneratedProtocolMessageType('UserChangeUsername', (_message.Message,), dict(
  DESCRIPTOR = _USERCHANGEUSERNAME,
  __module__ = 'LogModel_pb2'
  # @@protoc_insertion_point(class_scope:PBData.UserChangeUsername)
  ))
_sym_db.RegisterMessage(UserChangeUsername)

UserChangePassword = _reflection.GeneratedProtocolMessageType('UserChangePassword', (_message.Message,), dict(
  DESCRIPTOR = _USERCHANGEPASSWORD,
  __module__ = 'LogModel_pb2'
  # @@protoc_insertion_point(class_scope:PBData.UserChangePassword)
  ))
_sym_db.RegisterMessage(UserChangePassword)

FbConnectLog = _reflection.GeneratedProtocolMessageType('FbConnectLog', (_message.Message,), dict(
  DESCRIPTOR = _FBCONNECTLOG,
  __module__ = 'LogModel_pb2'
  # @@protoc_insertion_point(class_scope:PBData.FbConnectLog)
  ))
_sym_db.RegisterMessage(FbConnectLog)


# @@protoc_insertion_point(module_scope)