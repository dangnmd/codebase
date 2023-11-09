# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: User.proto

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
  name='User.proto',
  package='PBData',
  serialized_pb=_b('\n\nUser.proto\x12\x06PBData\"\x90\x01\n\x0bUserAccount\x12\x0b\n\x03uid\x18\x01 \x01(\x04\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x0c\n\x04salt\x18\x03 \x01(\t\x12\x10\n\x08password\x18\x04 \x01(\t\x12\x12\n\npassword_s\x18\x05 \x01(\r\x12\x0e\n\x06status\x18\x06 \x01(\x04\x12\r\n\x05\x65mail\x18\x07 \x01(\t\x12\x0f\n\x07\x65mail_v\x18\x08 \x01(\r\"\xb9\x01\n\x0bUserProfile\x12\x0b\n\x03uid\x18\x01 \x01(\x04\x12\x0e\n\x06gender\x18\x02 \x01(\r\x12\x0c\n\x04\x62\x64\x61y\x18\x03 \x01(\t\x12\x0f\n\x07regdate\x18\x04 \x01(\r\x12\r\n\x05regip\x18\x05 \x01(\t\x12\x10\n\x08location\x18\x06 \x01(\t\x12\x13\n\x0b\x61\x63\x63_country\x18\x07 \x01(\t\x12\x10\n\x08nickname\x18\x08 \x01(\t\x12\x11\n\tavatar_id\x18\t \x01(\x0c\x12\x13\n\x0bupdate_time\x18\n \x01(\r\"E\n\tUserShell\x12\x11\n\tavailable\x18\x01 \x01(\x05\x12\x12\n\ntopup_time\x18\x02 \x01(\r\x12\x11\n\tshop_time\x18\x03 \x01(\r\"\xcc\x01\n\nUserCredit\x12\x0b\n\x03uid\x18\x01 \x01(\r\x12\x0e\n\x06\x63redit\x18\x02 \x01(\r\x12\x13\n\x0bused_credit\x18\x03 \x01(\r\x12\x19\n\x11\x63redit_updatetime\x18\x04 \x01(\r\x12\x12\n\nfirst_time\x18\x05 \x01(\r\x12\x11\n\tlast_time\x18\x06 \x01(\r\x12\x12\n\nrepay_time\x18\x07 \x01(\r\x12\x0e\n\x06status\x18\x08 \x01(\r\x12\x12\n\nmax_credit\x18\t \x01(\x05\x12\x12\n\nbad_credit\x18\n \x01(\r\"\xe9\x01\n\x0bUserOtpSeed\x12\x0b\n\x03uid\x18\x01 \x01(\r\x12\x0c\n\x04seed\x18\x02 \x01(\t\x12\x14\n\x0c\x63ountry_code\x18\x03 \x01(\t\x12\x11\n\tmobile_no\x18\x04 \x01(\t\x12\x15\n\rmobile_enable\x18\x05 \x01(\x05\x12\x1a\n\x12\x61uthenticator_type\x18\x06 \x01(\x05\x12\x1c\n\x14\x61uthenticator_enable\x18\x07 \x01(\x05\x12\x1d\n\x15twostep_verify_enable\x18\x08 \x01(\x05\x12\x12\n\ncreatetime\x18\t \x01(\r\x12\x12\n\nupdatetime\x18\n \x01(\r\"J\n\x0cUserOtpToken\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0b\n\x03uid\x18\x02 \x01(\r\x12\r\n\x05token\x18\x03 \x01(\t\x12\x12\n\ncreatetime\x18\x04 \x01(\r\"o\n\x14UserOtpMobileBinding\x12\x0b\n\x03uid\x18\x01 \x01(\r\x12\x14\n\x0c\x63ountry_code\x18\x02 \x01(\t\x12\x11\n\tmobile_no\x18\x03 \x01(\t\x12\x11\n\tbind_time\x18\x04 \x01(\r\x12\x0e\n\x06status\x18\x05 \x01(\r\"s\n\x0fOtpSpcodeConfig\x12\x0e\n\x06spcode\x18\x01 \x01(\r\x12\x0e\n\x06spname\x18\x02 \x01(\t\x12\x0e\n\x06\x65nable\x18\x03 \x01(\r\x12\x16\n\x0euserdailylimit\x18\x04 \x01(\r\x12\x18\n\x10mobiledailylimit\x18\x05 \x01(\r\"\x87\x02\n\nUserDetail\x12\x0b\n\x03uid\x18\x01 \x01(\x04\x12\x12\n\nfirst_name\x18\x02 \x01(\t\x12\x11\n\tlast_name\x18\x03 \x01(\t\x12\x13\n\x0bmiddle_name\x18\x04 \x01(\t\x12\r\n\x05ic_no\x18\x05 \x01(\t\x12\x10\n\x08hometown\x18\x06 \x01(\r\x12\x11\n\tresidence\x18\x07 \x01(\r\x12\x0f\n\x07\x61\x64\x64ress\x18\x08 \x01(\t\x12\x10\n\x08postcode\x18\t \x01(\t\x12\x11\n\teducation\x18\n \x01(\r\x12\x0f\n\x07\x63ollege\x18\x0b \x01(\t\x12\x12\n\nhighschool\x18\x0c \x01(\t\x12\x0f\n\x07\x63ompany\x18\r \x01(\t\x12\x10\n\x08verified\x18\x0e \x01(\r\"\xfc\x01\n\x12RegisterUserParams\x12\x0b\n\x03uid\x18\x01 \x01(\x04\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x0c\n\x04salt\x18\x03 \x01(\t\x12\x10\n\x08password\x18\x04 \x01(\t\x12\x12\n\npassword_s\x18\x05 \x01(\r\x12\x0e\n\x06status\x18\x06 \x01(\x04\x12\r\n\x05\x65mail\x18\x07 \x01(\t\x12\x0f\n\x07\x65mail_v\x18\x08 \x01(\r\x12\x0e\n\x06gender\x18\t \x01(\r\x12\x0c\n\x04\x62\x64\x61y\x18\n \x01(\t\x12\x0f\n\x07regdate\x18\x0b \x01(\r\x12\r\n\x05regip\x18\x0c \x01(\t\x12\x10\n\x08location\x18\r \x01(\t\x12\x13\n\x0b\x61\x63\x63_country\x18\x0e \x01(\t')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_USERACCOUNT = _descriptor.Descriptor(
  name='UserAccount',
  full_name='PBData.UserAccount',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='PBData.UserAccount.uid', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='username', full_name='PBData.UserAccount.username', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='salt', full_name='PBData.UserAccount.salt', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='password', full_name='PBData.UserAccount.password', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='password_s', full_name='PBData.UserAccount.password_s', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='status', full_name='PBData.UserAccount.status', index=5,
      number=6, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='email', full_name='PBData.UserAccount.email', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='email_v', full_name='PBData.UserAccount.email_v', index=7,
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
  serialized_start=23,
  serialized_end=167,
)


_USERPROFILE = _descriptor.Descriptor(
  name='UserProfile',
  full_name='PBData.UserProfile',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='PBData.UserProfile.uid', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gender', full_name='PBData.UserProfile.gender', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bday', full_name='PBData.UserProfile.bday', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='regdate', full_name='PBData.UserProfile.regdate', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='regip', full_name='PBData.UserProfile.regip', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='location', full_name='PBData.UserProfile.location', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='acc_country', full_name='PBData.UserProfile.acc_country', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='nickname', full_name='PBData.UserProfile.nickname', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='avatar_id', full_name='PBData.UserProfile.avatar_id', index=8,
      number=9, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='update_time', full_name='PBData.UserProfile.update_time', index=9,
      number=10, type=13, cpp_type=3, label=1,
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
  serialized_start=170,
  serialized_end=355,
)


_USERSHELL = _descriptor.Descriptor(
  name='UserShell',
  full_name='PBData.UserShell',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='available', full_name='PBData.UserShell.available', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='topup_time', full_name='PBData.UserShell.topup_time', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='shop_time', full_name='PBData.UserShell.shop_time', index=2,
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
  serialized_start=357,
  serialized_end=426,
)


_USERCREDIT = _descriptor.Descriptor(
  name='UserCredit',
  full_name='PBData.UserCredit',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='PBData.UserCredit.uid', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='credit', full_name='PBData.UserCredit.credit', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='used_credit', full_name='PBData.UserCredit.used_credit', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='credit_updatetime', full_name='PBData.UserCredit.credit_updatetime', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='first_time', full_name='PBData.UserCredit.first_time', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='last_time', full_name='PBData.UserCredit.last_time', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='repay_time', full_name='PBData.UserCredit.repay_time', index=6,
      number=7, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='status', full_name='PBData.UserCredit.status', index=7,
      number=8, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='max_credit', full_name='PBData.UserCredit.max_credit', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bad_credit', full_name='PBData.UserCredit.bad_credit', index=9,
      number=10, type=13, cpp_type=3, label=1,
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
  serialized_start=429,
  serialized_end=633,
)


_USEROTPSEED = _descriptor.Descriptor(
  name='UserOtpSeed',
  full_name='PBData.UserOtpSeed',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='PBData.UserOtpSeed.uid', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seed', full_name='PBData.UserOtpSeed.seed', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='country_code', full_name='PBData.UserOtpSeed.country_code', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mobile_no', full_name='PBData.UserOtpSeed.mobile_no', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mobile_enable', full_name='PBData.UserOtpSeed.mobile_enable', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='authenticator_type', full_name='PBData.UserOtpSeed.authenticator_type', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='authenticator_enable', full_name='PBData.UserOtpSeed.authenticator_enable', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='twostep_verify_enable', full_name='PBData.UserOtpSeed.twostep_verify_enable', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='createtime', full_name='PBData.UserOtpSeed.createtime', index=8,
      number=9, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='updatetime', full_name='PBData.UserOtpSeed.updatetime', index=9,
      number=10, type=13, cpp_type=3, label=1,
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
  serialized_start=636,
  serialized_end=869,
)


_USEROTPTOKEN = _descriptor.Descriptor(
  name='UserOtpToken',
  full_name='PBData.UserOtpToken',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='PBData.UserOtpToken.id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='uid', full_name='PBData.UserOtpToken.uid', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='token', full_name='PBData.UserOtpToken.token', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='createtime', full_name='PBData.UserOtpToken.createtime', index=3,
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
  serialized_start=871,
  serialized_end=945,
)


_USEROTPMOBILEBINDING = _descriptor.Descriptor(
  name='UserOtpMobileBinding',
  full_name='PBData.UserOtpMobileBinding',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='PBData.UserOtpMobileBinding.uid', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='country_code', full_name='PBData.UserOtpMobileBinding.country_code', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mobile_no', full_name='PBData.UserOtpMobileBinding.mobile_no', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bind_time', full_name='PBData.UserOtpMobileBinding.bind_time', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='status', full_name='PBData.UserOtpMobileBinding.status', index=4,
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
  serialized_start=947,
  serialized_end=1058,
)


_OTPSPCODECONFIG = _descriptor.Descriptor(
  name='OtpSpcodeConfig',
  full_name='PBData.OtpSpcodeConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='spcode', full_name='PBData.OtpSpcodeConfig.spcode', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='spname', full_name='PBData.OtpSpcodeConfig.spname', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='enable', full_name='PBData.OtpSpcodeConfig.enable', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='userdailylimit', full_name='PBData.OtpSpcodeConfig.userdailylimit', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mobiledailylimit', full_name='PBData.OtpSpcodeConfig.mobiledailylimit', index=4,
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
  serialized_start=1060,
  serialized_end=1175,
)


_USERDETAIL = _descriptor.Descriptor(
  name='UserDetail',
  full_name='PBData.UserDetail',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='PBData.UserDetail.uid', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='first_name', full_name='PBData.UserDetail.first_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='last_name', full_name='PBData.UserDetail.last_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='middle_name', full_name='PBData.UserDetail.middle_name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ic_no', full_name='PBData.UserDetail.ic_no', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='hometown', full_name='PBData.UserDetail.hometown', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='residence', full_name='PBData.UserDetail.residence', index=6,
      number=7, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='address', full_name='PBData.UserDetail.address', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='postcode', full_name='PBData.UserDetail.postcode', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='education', full_name='PBData.UserDetail.education', index=9,
      number=10, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='college', full_name='PBData.UserDetail.college', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='highschool', full_name='PBData.UserDetail.highschool', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='company', full_name='PBData.UserDetail.company', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='verified', full_name='PBData.UserDetail.verified', index=13,
      number=14, type=13, cpp_type=3, label=1,
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
  serialized_start=1178,
  serialized_end=1441,
)


_REGISTERUSERPARAMS = _descriptor.Descriptor(
  name='RegisterUserParams',
  full_name='PBData.RegisterUserParams',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='PBData.RegisterUserParams.uid', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='username', full_name='PBData.RegisterUserParams.username', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='salt', full_name='PBData.RegisterUserParams.salt', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='password', full_name='PBData.RegisterUserParams.password', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='password_s', full_name='PBData.RegisterUserParams.password_s', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='status', full_name='PBData.RegisterUserParams.status', index=5,
      number=6, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='email', full_name='PBData.RegisterUserParams.email', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='email_v', full_name='PBData.RegisterUserParams.email_v', index=7,
      number=8, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gender', full_name='PBData.RegisterUserParams.gender', index=8,
      number=9, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bday', full_name='PBData.RegisterUserParams.bday', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='regdate', full_name='PBData.RegisterUserParams.regdate', index=10,
      number=11, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='regip', full_name='PBData.RegisterUserParams.regip', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='location', full_name='PBData.RegisterUserParams.location', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='acc_country', full_name='PBData.RegisterUserParams.acc_country', index=13,
      number=14, type=9, cpp_type=9, label=1,
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
  serialized_start=1444,
  serialized_end=1696,
)

DESCRIPTOR.message_types_by_name['UserAccount'] = _USERACCOUNT
DESCRIPTOR.message_types_by_name['UserProfile'] = _USERPROFILE
DESCRIPTOR.message_types_by_name['UserShell'] = _USERSHELL
DESCRIPTOR.message_types_by_name['UserCredit'] = _USERCREDIT
DESCRIPTOR.message_types_by_name['UserOtpSeed'] = _USEROTPSEED
DESCRIPTOR.message_types_by_name['UserOtpToken'] = _USEROTPTOKEN
DESCRIPTOR.message_types_by_name['UserOtpMobileBinding'] = _USEROTPMOBILEBINDING
DESCRIPTOR.message_types_by_name['OtpSpcodeConfig'] = _OTPSPCODECONFIG
DESCRIPTOR.message_types_by_name['UserDetail'] = _USERDETAIL
DESCRIPTOR.message_types_by_name['RegisterUserParams'] = _REGISTERUSERPARAMS

UserAccount = _reflection.GeneratedProtocolMessageType('UserAccount', (_message.Message,), dict(
  DESCRIPTOR = _USERACCOUNT,
  __module__ = 'User_pb2'
  # @@protoc_insertion_point(class_scope:PBData.UserAccount)
  ))
_sym_db.RegisterMessage(UserAccount)

UserProfile = _reflection.GeneratedProtocolMessageType('UserProfile', (_message.Message,), dict(
  DESCRIPTOR = _USERPROFILE,
  __module__ = 'User_pb2'
  # @@protoc_insertion_point(class_scope:PBData.UserProfile)
  ))
_sym_db.RegisterMessage(UserProfile)

UserShell = _reflection.GeneratedProtocolMessageType('UserShell', (_message.Message,), dict(
  DESCRIPTOR = _USERSHELL,
  __module__ = 'User_pb2'
  # @@protoc_insertion_point(class_scope:PBData.UserShell)
  ))
_sym_db.RegisterMessage(UserShell)

UserCredit = _reflection.GeneratedProtocolMessageType('UserCredit', (_message.Message,), dict(
  DESCRIPTOR = _USERCREDIT,
  __module__ = 'User_pb2'
  # @@protoc_insertion_point(class_scope:PBData.UserCredit)
  ))
_sym_db.RegisterMessage(UserCredit)

UserOtpSeed = _reflection.GeneratedProtocolMessageType('UserOtpSeed', (_message.Message,), dict(
  DESCRIPTOR = _USEROTPSEED,
  __module__ = 'User_pb2'
  # @@protoc_insertion_point(class_scope:PBData.UserOtpSeed)
  ))
_sym_db.RegisterMessage(UserOtpSeed)

UserOtpToken = _reflection.GeneratedProtocolMessageType('UserOtpToken', (_message.Message,), dict(
  DESCRIPTOR = _USEROTPTOKEN,
  __module__ = 'User_pb2'
  # @@protoc_insertion_point(class_scope:PBData.UserOtpToken)
  ))
_sym_db.RegisterMessage(UserOtpToken)

UserOtpMobileBinding = _reflection.GeneratedProtocolMessageType('UserOtpMobileBinding', (_message.Message,), dict(
  DESCRIPTOR = _USEROTPMOBILEBINDING,
  __module__ = 'User_pb2'
  # @@protoc_insertion_point(class_scope:PBData.UserOtpMobileBinding)
  ))
_sym_db.RegisterMessage(UserOtpMobileBinding)

OtpSpcodeConfig = _reflection.GeneratedProtocolMessageType('OtpSpcodeConfig', (_message.Message,), dict(
  DESCRIPTOR = _OTPSPCODECONFIG,
  __module__ = 'User_pb2'
  # @@protoc_insertion_point(class_scope:PBData.OtpSpcodeConfig)
  ))
_sym_db.RegisterMessage(OtpSpcodeConfig)

UserDetail = _reflection.GeneratedProtocolMessageType('UserDetail', (_message.Message,), dict(
  DESCRIPTOR = _USERDETAIL,
  __module__ = 'User_pb2'
  # @@protoc_insertion_point(class_scope:PBData.UserDetail)
  ))
_sym_db.RegisterMessage(UserDetail)

RegisterUserParams = _reflection.GeneratedProtocolMessageType('RegisterUserParams', (_message.Message,), dict(
  DESCRIPTOR = _REGISTERUSERPARAMS,
  __module__ = 'User_pb2'
  # @@protoc_insertion_point(class_scope:PBData.RegisterUserParams)
  ))
_sym_db.RegisterMessage(RegisterUserParams)


# @@protoc_insertion_point(module_scope)