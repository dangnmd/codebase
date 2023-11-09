# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Clan.proto

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
  name='Clan.proto',
  package='PBData',
  serialized_pb=_b('\n\nClan.proto\x12\x06PBData\"\xc1\x02\n\x08\x43lanInfo\x12\x0f\n\x07\x63lan_id\x18\x01 \x02(\x05\x12\x11\n\tclan_name\x18\x02 \x01(\t\x12\x15\n\rclan_nickname\x18\x03 \x01(\t\x12\x0f\n\x07\x63ountry\x18\x04 \x01(\t\x12\x0c\n\x04game\x18\x05 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x06 \x01(\t\x12\x14\n\x0c\x61nnouncement\x18\x07 \x01(\t\x12\x0e\n\x06lordid\x18\x08 \x01(\x05\x12\x12\n\nmembersize\x18\t \x01(\x05\x12\x0f\n\x07maxsize\x18\n \x01(\x05\x12\x12\n\ncreatedate\x18\x0b \x01(\x05\x12\x12\n\nupdatetime\x18\x0c \x01(\x05\x12\x0e\n\x06\x62\x61nner\x18\r \x01(\x05\x12\x0c\n\x04logo\x18\x0e \x01(\x05\x12\x10\n\x08lordname\x18\x0f \x01(\t\x12\x12\n\next_clanid\x18\x10 \x01(\x05\x12\x0f\n\x07game_id\x18\x11 \x01(\r\"n\n\nClanMember\x12\x0f\n\x07\x63lan_id\x18\x01 \x02(\x05\x12\x0b\n\x03uid\x18\x02 \x02(\x05\x12\r\n\x05utype\x18\x03 \x01(\x05\x12\r\n\x05title\x18\x04 \x01(\t\x12\x10\n\x08jointime\x18\x05 \x01(\x05\x12\x12\n\nupdatetime\x18\x06 \x01(\x05\"\x95\x01\n\x0b\x43lanRequest\x12\x0f\n\x07\x63lan_id\x18\x01 \x01(\x05\x12\x0b\n\x03uid\x18\x02 \x02(\x05\x12\x11\n\tinviterid\x18\x03 \x02(\x05\x12\x14\n\x0crequest_type\x18\x04 \x01(\x05\x12\x16\n\x0erequest_status\x18\x05 \x01(\x05\x12\x12\n\nupdatetime\x18\x06 \x01(\x05\x12\x13\n\x0b\x64\x65scription\x18\x07 \x01(\t\"g\n\nClanInvite\x12\x0f\n\x07\x63lan_id\x18\x01 \x02(\r\x12\x11\n\tinviterid\x18\x02 \x01(\r\x12\x11\n\tinviteeid\x18\x03 \x02(\r\x12\x12\n\nupdatetime\x18\x04 \x01(\r\x12\x0e\n\x06reason\x18\x05 \x01(\t')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_CLANINFO = _descriptor.Descriptor(
  name='ClanInfo',
  full_name='PBData.ClanInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='clan_id', full_name='PBData.ClanInfo.clan_id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='clan_name', full_name='PBData.ClanInfo.clan_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='clan_nickname', full_name='PBData.ClanInfo.clan_nickname', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='country', full_name='PBData.ClanInfo.country', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='game', full_name='PBData.ClanInfo.game', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='description', full_name='PBData.ClanInfo.description', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='announcement', full_name='PBData.ClanInfo.announcement', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lordid', full_name='PBData.ClanInfo.lordid', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='membersize', full_name='PBData.ClanInfo.membersize', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='maxsize', full_name='PBData.ClanInfo.maxsize', index=9,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='createdate', full_name='PBData.ClanInfo.createdate', index=10,
      number=11, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='updatetime', full_name='PBData.ClanInfo.updatetime', index=11,
      number=12, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='banner', full_name='PBData.ClanInfo.banner', index=12,
      number=13, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='logo', full_name='PBData.ClanInfo.logo', index=13,
      number=14, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lordname', full_name='PBData.ClanInfo.lordname', index=14,
      number=15, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ext_clanid', full_name='PBData.ClanInfo.ext_clanid', index=15,
      number=16, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='game_id', full_name='PBData.ClanInfo.game_id', index=16,
      number=17, type=13, cpp_type=3, label=1,
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
  serialized_start=23,
  serialized_end=344,
)


_CLANMEMBER = _descriptor.Descriptor(
  name='ClanMember',
  full_name='PBData.ClanMember',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='clan_id', full_name='PBData.ClanMember.clan_id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='uid', full_name='PBData.ClanMember.uid', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='utype', full_name='PBData.ClanMember.utype', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='title', full_name='PBData.ClanMember.title', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='jointime', full_name='PBData.ClanMember.jointime', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='updatetime', full_name='PBData.ClanMember.updatetime', index=5,
      number=6, type=5, cpp_type=1, label=1,
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
  serialized_start=346,
  serialized_end=456,
)


_CLANREQUEST = _descriptor.Descriptor(
  name='ClanRequest',
  full_name='PBData.ClanRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='clan_id', full_name='PBData.ClanRequest.clan_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='uid', full_name='PBData.ClanRequest.uid', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='inviterid', full_name='PBData.ClanRequest.inviterid', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='request_type', full_name='PBData.ClanRequest.request_type', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='request_status', full_name='PBData.ClanRequest.request_status', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='updatetime', full_name='PBData.ClanRequest.updatetime', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='description', full_name='PBData.ClanRequest.description', index=6,
      number=7, type=9, cpp_type=9, label=1,
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
  serialized_start=459,
  serialized_end=608,
)


_CLANINVITE = _descriptor.Descriptor(
  name='ClanInvite',
  full_name='PBData.ClanInvite',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='clan_id', full_name='PBData.ClanInvite.clan_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='inviterid', full_name='PBData.ClanInvite.inviterid', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='inviteeid', full_name='PBData.ClanInvite.inviteeid', index=2,
      number=3, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='updatetime', full_name='PBData.ClanInvite.updatetime', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='reason', full_name='PBData.ClanInvite.reason', index=4,
      number=5, type=9, cpp_type=9, label=1,
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
  serialized_start=610,
  serialized_end=713,
)

DESCRIPTOR.message_types_by_name['ClanInfo'] = _CLANINFO
DESCRIPTOR.message_types_by_name['ClanMember'] = _CLANMEMBER
DESCRIPTOR.message_types_by_name['ClanRequest'] = _CLANREQUEST
DESCRIPTOR.message_types_by_name['ClanInvite'] = _CLANINVITE

ClanInfo = _reflection.GeneratedProtocolMessageType('ClanInfo', (_message.Message,), dict(
  DESCRIPTOR = _CLANINFO,
  __module__ = 'Clan_pb2'
  # @@protoc_insertion_point(class_scope:PBData.ClanInfo)
  ))
_sym_db.RegisterMessage(ClanInfo)

ClanMember = _reflection.GeneratedProtocolMessageType('ClanMember', (_message.Message,), dict(
  DESCRIPTOR = _CLANMEMBER,
  __module__ = 'Clan_pb2'
  # @@protoc_insertion_point(class_scope:PBData.ClanMember)
  ))
_sym_db.RegisterMessage(ClanMember)

ClanRequest = _reflection.GeneratedProtocolMessageType('ClanRequest', (_message.Message,), dict(
  DESCRIPTOR = _CLANREQUEST,
  __module__ = 'Clan_pb2'
  # @@protoc_insertion_point(class_scope:PBData.ClanRequest)
  ))
_sym_db.RegisterMessage(ClanRequest)

ClanInvite = _reflection.GeneratedProtocolMessageType('ClanInvite', (_message.Message,), dict(
  DESCRIPTOR = _CLANINVITE,
  __module__ = 'Clan_pb2'
  # @@protoc_insertion_point(class_scope:PBData.ClanInvite)
  ))
_sym_db.RegisterMessage(ClanInvite)


# @@protoc_insertion_point(module_scope)