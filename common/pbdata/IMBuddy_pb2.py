# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: IMBuddy.proto

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
  name='IMBuddy.proto',
  package='PBData.IM',
  serialized_pb=_b('\n\rIMBuddy.proto\x12\tPBData.IM\"[\n\x05\x42uddy\x12\x0b\n\x03uid\x18\x01 \x02(\r\x12\x0f\n\x07\x62uddyid\x18\x02 \x02(\r\x12\x0e\n\x06\x63\x61teid\x18\x03 \x01(\r\x12\x10\n\x08relation\x18\x04 \x01(\r\x12\x12\n\ncreatedate\x18\x05 \x01(\r\"n\n\x0c\x42uddyRequest\x12\x0e\n\x06\x66romid\x18\x01 \x02(\r\x12\x0c\n\x04toid\x18\x02 \x02(\r\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0e\n\x06reason\x18\x04 \x01(\t\x12\x12\n\ncreatetime\x18\x05 \x01(\r\x12\x0e\n\x06\x63\x61teid\x18\x06 \x01(\r\"N\n\rBuddyCategory\x12\x0e\n\x06\x63\x61teid\x18\x01 \x02(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0b\n\x03uid\x18\x03 \x02(\r\x12\x12\n\ncreatedate\x18\x04 \x01(\r')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_BUDDY = _descriptor.Descriptor(
  name='Buddy',
  full_name='PBData.IM.Buddy',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='PBData.IM.Buddy.uid', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='buddyid', full_name='PBData.IM.Buddy.buddyid', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cateid', full_name='PBData.IM.Buddy.cateid', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='relation', full_name='PBData.IM.Buddy.relation', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='createdate', full_name='PBData.IM.Buddy.createdate', index=4,
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
  serialized_start=28,
  serialized_end=119,
)


_BUDDYREQUEST = _descriptor.Descriptor(
  name='BuddyRequest',
  full_name='PBData.IM.BuddyRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fromid', full_name='PBData.IM.BuddyRequest.fromid', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='toid', full_name='PBData.IM.BuddyRequest.toid', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='PBData.IM.BuddyRequest.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='reason', full_name='PBData.IM.BuddyRequest.reason', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='createtime', full_name='PBData.IM.BuddyRequest.createtime', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cateid', full_name='PBData.IM.BuddyRequest.cateid', index=5,
      number=6, type=13, cpp_type=3, label=1,
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
  serialized_start=121,
  serialized_end=231,
)


_BUDDYCATEGORY = _descriptor.Descriptor(
  name='BuddyCategory',
  full_name='PBData.IM.BuddyCategory',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cateid', full_name='PBData.IM.BuddyCategory.cateid', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='PBData.IM.BuddyCategory.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='uid', full_name='PBData.IM.BuddyCategory.uid', index=2,
      number=3, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='createdate', full_name='PBData.IM.BuddyCategory.createdate', index=3,
      number=4, type=13, cpp_type=3, label=1,
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
  serialized_start=233,
  serialized_end=311,
)

DESCRIPTOR.message_types_by_name['Buddy'] = _BUDDY
DESCRIPTOR.message_types_by_name['BuddyRequest'] = _BUDDYREQUEST
DESCRIPTOR.message_types_by_name['BuddyCategory'] = _BUDDYCATEGORY

Buddy = _reflection.GeneratedProtocolMessageType('Buddy', (_message.Message,), dict(
  DESCRIPTOR = _BUDDY,
  __module__ = 'IMBuddy_pb2'
  # @@protoc_insertion_point(class_scope:PBData.IM.Buddy)
  ))
_sym_db.RegisterMessage(Buddy)

BuddyRequest = _reflection.GeneratedProtocolMessageType('BuddyRequest', (_message.Message,), dict(
  DESCRIPTOR = _BUDDYREQUEST,
  __module__ = 'IMBuddy_pb2'
  # @@protoc_insertion_point(class_scope:PBData.IM.BuddyRequest)
  ))
_sym_db.RegisterMessage(BuddyRequest)

BuddyCategory = _reflection.GeneratedProtocolMessageType('BuddyCategory', (_message.Message,), dict(
  DESCRIPTOR = _BUDDYCATEGORY,
  __module__ = 'IMBuddy_pb2'
  # @@protoc_insertion_point(class_scope:PBData.IM.BuddyCategory)
  ))
_sym_db.RegisterMessage(BuddyCategory)


# @@protoc_insertion_point(module_scope)
