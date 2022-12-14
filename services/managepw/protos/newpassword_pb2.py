# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: newpassword.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11newpassword.proto\x12\x05newpw\"^\n\tPwRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06length\x18\x02 \x01(\x05\x12\x0f\n\x07service\x18\x03 \x01(\t\x12\x0f\n\x07symbols\x18\x04 \x01(\x08\x12\x11\n\thastoSave\x18\x05 \x01(\x08\"&\n\x07PwReply\x12\n\n\x02pw\x18\x01 \x01(\t\x12\x0f\n\x07isSaved\x18\x02 \x01(\x08\x32\x99\x02\n\x08Password\x12\x30\n\nGetNewPass\x12\x10.newpw.PwRequest\x1a\x0e.newpw.PwReply\"\x00\x12\x33\n\rGetNewNumPass\x12\x10.newpw.PwRequest\x1a\x0e.newpw.PwReply\"\x00\x12\x35\n\x0fGetNewLowerPass\x12\x10.newpw.PwRequest\x1a\x0e.newpw.PwReply\"\x00\x12\x35\n\x0fGetNewUpperPass\x12\x10.newpw.PwRequest\x1a\x0e.newpw.PwReply\"\x00\x12\x38\n\x12GetNewAlphaNumPass\x12\x10.newpw.PwRequest\x1a\x0e.newpw.PwReply\"\x00\x42$\n\x0e/SDCC/servicesB\nNewPwProtoP\x01\xa2\x02\x03NPWb\x06proto3')



_PWREQUEST = DESCRIPTOR.message_types_by_name['PwRequest']
_PWREPLY = DESCRIPTOR.message_types_by_name['PwReply']
PwRequest = _reflection.GeneratedProtocolMessageType('PwRequest', (_message.Message,), {
  'DESCRIPTOR' : _PWREQUEST,
  '__module__' : 'newpassword_pb2'
  # @@protoc_insertion_point(class_scope:newpw.PwRequest)
  })
_sym_db.RegisterMessage(PwRequest)

PwReply = _reflection.GeneratedProtocolMessageType('PwReply', (_message.Message,), {
  'DESCRIPTOR' : _PWREPLY,
  '__module__' : 'newpassword_pb2'
  # @@protoc_insertion_point(class_scope:newpw.PwReply)
  })
_sym_db.RegisterMessage(PwReply)

_PASSWORD = DESCRIPTOR.services_by_name['Password']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\016/SDCC/servicesB\nNewPwProtoP\001\242\002\003NPW'
  _PWREQUEST._serialized_start=28
  _PWREQUEST._serialized_end=122
  _PWREPLY._serialized_start=124
  _PWREPLY._serialized_end=162
  _PASSWORD._serialized_start=165
  _PASSWORD._serialized_end=446
# @@protoc_insertion_point(module_scope)
