# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: groupmanager.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12groupmanager.proto\x12\x0cgroupmanager\"H\n\x12GroupCreateRequest\x12\x12\n\ngroup_name\x18\x01 \x01(\t\x12\x0e\n\x06\x65mails\x18\x02 \x03(\t\x12\x0e\n\x06\x61gency\x18\x03 \x01(\t\"%\n\x10GroupCreateReply\x12\x11\n\tisCreated\x18\x01 \x01(\x11\"!\n\x10GroupListRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\"s\n\x0eGroupListReply\x12\x34\n\x04list\x18\x01 \x03(\x0b\x32&.groupmanager.GroupListReply.ListEntry\x1a+\n\tListEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"G\n\x11\x43heckGroupRequest\x12\x12\n\ngroup_name\x18\x01 \x01(\t\x12\x0f\n\x07service\x18\x02 \x01(\t\x12\r\n\x05\x65mail\x18\x03 \x01(\t\"\'\n\x12\x43heckGroupResponse\x12\x11\n\tisChecked\x18\x01 \x01(\x08\x32\x81\x02\n\x0cGroupManager\x12Q\n\x0bgroupCreate\x12 .groupmanager.GroupCreateRequest\x1a\x1e.groupmanager.GroupCreateReply\"\x00\x12K\n\tgroupList\x12\x1e.groupmanager.GroupListRequest\x1a\x1c.groupmanager.GroupListReply\"\x00\x12Q\n\ncheckGroup\x12\x1f.groupmanager.CheckGroupRequest\x1a .groupmanager.CheckGroupResponse\"\x00\x42(\n\x0e/SDCC/servicesB\x0eGpManagerProtoP\x01\xa2\x02\x03GPMb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'groupmanager_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\016/SDCC/servicesB\016GpManagerProtoP\001\242\002\003GPM'
  _GROUPLISTREPLY_LISTENTRY._options = None
  _GROUPLISTREPLY_LISTENTRY._serialized_options = b'8\001'
  _GROUPCREATEREQUEST._serialized_start=36
  _GROUPCREATEREQUEST._serialized_end=108
  _GROUPCREATEREPLY._serialized_start=110
  _GROUPCREATEREPLY._serialized_end=147
  _GROUPLISTREQUEST._serialized_start=149
  _GROUPLISTREQUEST._serialized_end=182
  _GROUPLISTREPLY._serialized_start=184
  _GROUPLISTREPLY._serialized_end=299
  _GROUPLISTREPLY_LISTENTRY._serialized_start=256
  _GROUPLISTREPLY_LISTENTRY._serialized_end=299
  _CHECKGROUPREQUEST._serialized_start=301
  _CHECKGROUPREQUEST._serialized_end=372
  _CHECKGROUPRESPONSE._serialized_start=374
  _CHECKGROUPRESPONSE._serialized_end=413
  _GROUPMANAGER._serialized_start=416
  _GROUPMANAGER._serialized_end=673
# @@protoc_insertion_point(module_scope)
