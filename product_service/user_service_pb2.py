# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: user_service.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12user_service.proto\x12\x0cuser_service\"H\n\x13RegisterUserRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x10\n\x08password\x18\x03 \x01(\t\"\'\n\x14RegisterUserResponse\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\"6\n\x10LoginUserRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\")\n\x11LoginUserResponse\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t\"(\n\x15GetUserProfileRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\"J\n\x16GetUserProfileResponse\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\x10\n\x08username\x18\x02 \x01(\t\x12\r\n\x05\x65mail\x18\x03 \x01(\t2\x95\x02\n\x0bUserService\x12W\n\x0cRegisterUser\x12!.user_service.RegisterUserRequest\x1a\".user_service.RegisterUserResponse\"\x00\x12N\n\tLoginUser\x12\x1e.user_service.LoginUserRequest\x1a\x1f.user_service.LoginUserResponse\"\x00\x12]\n\x0eGetUserProfile\x12#.user_service.GetUserProfileRequest\x1a$.user_service.GetUserProfileResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'user_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_REGISTERUSERREQUEST']._serialized_start=36
  _globals['_REGISTERUSERREQUEST']._serialized_end=108
  _globals['_REGISTERUSERRESPONSE']._serialized_start=110
  _globals['_REGISTERUSERRESPONSE']._serialized_end=149
  _globals['_LOGINUSERREQUEST']._serialized_start=151
  _globals['_LOGINUSERREQUEST']._serialized_end=205
  _globals['_LOGINUSERRESPONSE']._serialized_start=207
  _globals['_LOGINUSERRESPONSE']._serialized_end=248
  _globals['_GETUSERPROFILEREQUEST']._serialized_start=250
  _globals['_GETUSERPROFILEREQUEST']._serialized_end=290
  _globals['_GETUSERPROFILERESPONSE']._serialized_start=292
  _globals['_GETUSERPROFILERESPONSE']._serialized_end=366
  _globals['_USERSERVICE']._serialized_start=369
  _globals['_USERSERVICE']._serialized_end=646
# @@protoc_insertion_point(module_scope)
