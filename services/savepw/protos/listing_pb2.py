# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: listing.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rlisting.proto\x12\x07listing\"\x1f\n\x0bListRequest\x12\x10\n\x08username\x18\x01 \x01(\t\"d\n\tListReply\x12*\n\x04list\x18\x01 \x03(\x0b\x32\x1c.listing.ListReply.ListEntry\x1a+\n\tListEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x32?\n\x07Listing\x12\x34\n\x06\x64oList\x12\x14.listing.ListRequest\x1a\x12.listing.ListReply\"\x00\x42&\n\x0e/SDCC/servicesB\x0cListingProtoP\x01\xa2\x02\x03LISb\x06proto3')



_LISTREQUEST = DESCRIPTOR.message_types_by_name['ListRequest']
_LISTREPLY = DESCRIPTOR.message_types_by_name['ListReply']
_LISTREPLY_LISTENTRY = _LISTREPLY.nested_types_by_name['ListEntry']
ListRequest = _reflection.GeneratedProtocolMessageType('ListRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTREQUEST,
  '__module__' : 'listing_pb2'
  # @@protoc_insertion_point(class_scope:listing.ListRequest)
  })
_sym_db.RegisterMessage(ListRequest)

ListReply = _reflection.GeneratedProtocolMessageType('ListReply', (_message.Message,), {

  'ListEntry' : _reflection.GeneratedProtocolMessageType('ListEntry', (_message.Message,), {
    'DESCRIPTOR' : _LISTREPLY_LISTENTRY,
    '__module__' : 'listing_pb2'
    # @@protoc_insertion_point(class_scope:listing.ListReply.ListEntry)
    })
  ,
  'DESCRIPTOR' : _LISTREPLY,
  '__module__' : 'listing_pb2'
  # @@protoc_insertion_point(class_scope:listing.ListReply)
  })
_sym_db.RegisterMessage(ListReply)
_sym_db.RegisterMessage(ListReply.ListEntry)

_LISTING = DESCRIPTOR.services_by_name['Listing']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\016/SDCC/servicesB\014ListingProtoP\001\242\002\003LIS'
  _LISTREPLY_LISTENTRY._options = None
  _LISTREPLY_LISTENTRY._serialized_options = b'8\001'
  _LISTREQUEST._serialized_start=26
  _LISTREQUEST._serialized_end=57
  _LISTREPLY._serialized_start=59
  _LISTREPLY._serialized_end=159
  _LISTREPLY_LISTENTRY._serialized_start=116
  _LISTREPLY_LISTENTRY._serialized_end=159
  _LISTING._serialized_start=161
  _LISTING._serialized_end=224
# @@protoc_insertion_point(module_scope)
