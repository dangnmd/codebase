# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pns.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='pns.proto',
  package='',
  serialized_pb=_b('\n\tpns.proto\"\xd1\x01\n\x0cNotification\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\t\x12\x13\n\x0b\x63lient_type\x18\x02 \x01(\r\x12\x14\n\x0c\x64\x65vice_token\x18\x03 \x01(\x0c\x12\x13\n\x0b\x65xpire_time\x18\x04 \x01(\r\x12\x0f\n\x07message\x18\x05 \x01(\t\x12\r\n\x05\x62\x61\x64ge\x18\x06 \x01(\r\x12\r\n\x05sound\x18\x07 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x08 \x01(\t\x12\x0c\n\x04\x66lag\x18\t \x01(\r\x12\x14\n\x0cservice_type\x18\x0e \x01(\r\x12\x10\n\x08priority\x18\x0f \x01(\r\"\x96\x01\n\x0bPNSResponse\x12\x12\n\nerror_code\x18\x01 \x01(\r\"s\n\tErrorCode\x12\x0f\n\x0bPNS_SUCCESS\x10\x00\x12\x16\n\x12PNS_PARAMS_INVALID\x10\x01\x12\x10\n\x0cPNS_OVERSIZE\x10\x02\x12\x14\n\x10PNS_SERVER_ERROR\x10\x03\x12\x15\n\x11PNS_SERVER_REJECT\x10\x04\"N\n\x11InvalidTokenQuery\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\t\x12\x13\n\x0b\x63lient_type\x18\x02 \x01(\r\x12\x14\n\x0cservice_type\x18\x03 \x01(\r\"E\n\x05Token\x12\x13\n\x0b\x63lient_type\x18\x01 \x01(\r\x12\x11\n\ttimestamp\x18\x02 \x01(\r\x12\x14\n\x0c\x64\x65vice_token\x18\x03 \x01(\x0c\"\'\n\rInvalidTokens\x12\x16\n\x06tokens\x18\x01 \x03(\x0b\x32\x06.Token\"\"\n\x10\x41ppUpdateRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\t*V\n\x07\x43ommand\x12\x19\n\x15\x43MD_PUSH_NOTIFICATION\x10\x10\x12\x1c\n\x18\x43MD_QUERY_INVALID_TOKENS\x10@\x12\x12\n\x0e\x43MD_APP_UPDATE\x10P*,\n\nClientType\x12\x0c\n\x08TYPE_IOS\x10\x00\x12\x10\n\x0cTYPE_ANDROID\x10\x01*C\n\x0bServiceType\x12\x10\n\x0cSERVICE_APNS\x10\x00\x12\x10\n\x0cSERVICE_GPNS\x10\x01\x12\x10\n\x0cSERVICE_GCMS\x10\x02*7\n\rPriorityLevel\x12\x13\n\x0fPRIORITY_NORMAL\x10\x01\x12\x11\n\rPRIORITY_HIGH\x10\x02')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

_COMMAND = _descriptor.EnumDescriptor(
  name='Command',
  full_name='Command',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CMD_PUSH_NOTIFICATION', index=0, number=16,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CMD_QUERY_INVALID_TOKENS', index=1, number=64,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CMD_APP_UPDATE', index=2, number=80,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=606,
  serialized_end=692,
)
_sym_db.RegisterEnumDescriptor(_COMMAND)

Command = enum_type_wrapper.EnumTypeWrapper(_COMMAND)
_CLIENTTYPE = _descriptor.EnumDescriptor(
  name='ClientType',
  full_name='ClientType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='TYPE_IOS', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TYPE_ANDROID', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=694,
  serialized_end=738,
)
_sym_db.RegisterEnumDescriptor(_CLIENTTYPE)

ClientType = enum_type_wrapper.EnumTypeWrapper(_CLIENTTYPE)
_SERVICETYPE = _descriptor.EnumDescriptor(
  name='ServiceType',
  full_name='ServiceType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SERVICE_APNS', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SERVICE_GPNS', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SERVICE_GCMS', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=740,
  serialized_end=807,
)
_sym_db.RegisterEnumDescriptor(_SERVICETYPE)

ServiceType = enum_type_wrapper.EnumTypeWrapper(_SERVICETYPE)
_PRIORITYLEVEL = _descriptor.EnumDescriptor(
  name='PriorityLevel',
  full_name='PriorityLevel',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='PRIORITY_NORMAL', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PRIORITY_HIGH', index=1, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=809,
  serialized_end=864,
)
_sym_db.RegisterEnumDescriptor(_PRIORITYLEVEL)

PriorityLevel = enum_type_wrapper.EnumTypeWrapper(_PRIORITYLEVEL)
CMD_PUSH_NOTIFICATION = 16
CMD_QUERY_INVALID_TOKENS = 64
CMD_APP_UPDATE = 80
TYPE_IOS = 0
TYPE_ANDROID = 1
SERVICE_APNS = 0
SERVICE_GPNS = 1
SERVICE_GCMS = 2
PRIORITY_NORMAL = 1
PRIORITY_HIGH = 2


_PNSRESPONSE_ERRORCODE = _descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='PNSResponse.ErrorCode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='PNS_SUCCESS', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PNS_PARAMS_INVALID', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PNS_OVERSIZE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PNS_SERVER_ERROR', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PNS_SERVER_REJECT', index=4, number=4,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=261,
  serialized_end=376,
)
_sym_db.RegisterEnumDescriptor(_PNSRESPONSE_ERRORCODE)


_NOTIFICATION = _descriptor.Descriptor(
  name='Notification',
  full_name='Notification',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_id', full_name='Notification.app_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='client_type', full_name='Notification.client_type', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='device_token', full_name='Notification.device_token', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='expire_time', full_name='Notification.expire_time', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='message', full_name='Notification.message', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='badge', full_name='Notification.badge', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sound', full_name='Notification.sound', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='Notification.data', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='flag', full_name='Notification.flag', index=8,
      number=9, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='service_type', full_name='Notification.service_type', index=9,
      number=14, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='priority', full_name='Notification.priority', index=10,
      number=15, type=13, cpp_type=3, label=1,
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
  serialized_start=14,
  serialized_end=223,
)


_PNSRESPONSE = _descriptor.Descriptor(
  name='PNSResponse',
  full_name='PNSResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='error_code', full_name='PNSResponse.error_code', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _PNSRESPONSE_ERRORCODE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=226,
  serialized_end=376,
)


_INVALIDTOKENQUERY = _descriptor.Descriptor(
  name='InvalidTokenQuery',
  full_name='InvalidTokenQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_id', full_name='InvalidTokenQuery.app_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='client_type', full_name='InvalidTokenQuery.client_type', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='service_type', full_name='InvalidTokenQuery.service_type', index=2,
      number=3, type=13, cpp_type=3, label=1,
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
  serialized_start=378,
  serialized_end=456,
)


_TOKEN = _descriptor.Descriptor(
  name='Token',
  full_name='Token',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='client_type', full_name='Token.client_type', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='Token.timestamp', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='device_token', full_name='Token.device_token', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
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
  serialized_start=458,
  serialized_end=527,
)


_INVALIDTOKENS = _descriptor.Descriptor(
  name='InvalidTokens',
  full_name='InvalidTokens',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='tokens', full_name='InvalidTokens.tokens', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=529,
  serialized_end=568,
)


_APPUPDATEREQUEST = _descriptor.Descriptor(
  name='AppUpdateRequest',
  full_name='AppUpdateRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_id', full_name='AppUpdateRequest.app_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=570,
  serialized_end=604,
)

_PNSRESPONSE_ERRORCODE.containing_type = _PNSRESPONSE
_INVALIDTOKENS.fields_by_name['tokens'].message_type = _TOKEN
DESCRIPTOR.message_types_by_name['Notification'] = _NOTIFICATION
DESCRIPTOR.message_types_by_name['PNSResponse'] = _PNSRESPONSE
DESCRIPTOR.message_types_by_name['InvalidTokenQuery'] = _INVALIDTOKENQUERY
DESCRIPTOR.message_types_by_name['Token'] = _TOKEN
DESCRIPTOR.message_types_by_name['InvalidTokens'] = _INVALIDTOKENS
DESCRIPTOR.message_types_by_name['AppUpdateRequest'] = _APPUPDATEREQUEST
DESCRIPTOR.enum_types_by_name['Command'] = _COMMAND
DESCRIPTOR.enum_types_by_name['ClientType'] = _CLIENTTYPE
DESCRIPTOR.enum_types_by_name['ServiceType'] = _SERVICETYPE
DESCRIPTOR.enum_types_by_name['PriorityLevel'] = _PRIORITYLEVEL

Notification = _reflection.GeneratedProtocolMessageType('Notification', (_message.Message,), dict(
  DESCRIPTOR = _NOTIFICATION,
  __module__ = 'pns_pb2'
  # @@protoc_insertion_point(class_scope:Notification)
  ))
_sym_db.RegisterMessage(Notification)

PNSResponse = _reflection.GeneratedProtocolMessageType('PNSResponse', (_message.Message,), dict(
  DESCRIPTOR = _PNSRESPONSE,
  __module__ = 'pns_pb2'
  # @@protoc_insertion_point(class_scope:PNSResponse)
  ))
_sym_db.RegisterMessage(PNSResponse)

InvalidTokenQuery = _reflection.GeneratedProtocolMessageType('InvalidTokenQuery', (_message.Message,), dict(
  DESCRIPTOR = _INVALIDTOKENQUERY,
  __module__ = 'pns_pb2'
  # @@protoc_insertion_point(class_scope:InvalidTokenQuery)
  ))
_sym_db.RegisterMessage(InvalidTokenQuery)

Token = _reflection.GeneratedProtocolMessageType('Token', (_message.Message,), dict(
  DESCRIPTOR = _TOKEN,
  __module__ = 'pns_pb2'
  # @@protoc_insertion_point(class_scope:Token)
  ))
_sym_db.RegisterMessage(Token)

InvalidTokens = _reflection.GeneratedProtocolMessageType('InvalidTokens', (_message.Message,), dict(
  DESCRIPTOR = _INVALIDTOKENS,
  __module__ = 'pns_pb2'
  # @@protoc_insertion_point(class_scope:InvalidTokens)
  ))
_sym_db.RegisterMessage(InvalidTokens)

AppUpdateRequest = _reflection.GeneratedProtocolMessageType('AppUpdateRequest', (_message.Message,), dict(
  DESCRIPTOR = _APPUPDATEREQUEST,
  __module__ = 'pns_pb2'
  # @@protoc_insertion_point(class_scope:AppUpdateRequest)
  ))
_sym_db.RegisterMessage(AppUpdateRequest)


# @@protoc_insertion_point(module_scope)
