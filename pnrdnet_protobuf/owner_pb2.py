# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: owner.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bowner.proto\"<\n\x05Owner\x12\x12\n\npublic_key\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x11\n\ttimestamp\x18\x03 \x01(\x04\")\n\x0eOwnerContainer\x12\x17\n\x07\x65ntries\x18\x01 \x03(\x0b\x32\x06.Ownerb\x06proto3')



_OWNER = DESCRIPTOR.message_types_by_name['Owner']
_OWNERCONTAINER = DESCRIPTOR.message_types_by_name['OwnerContainer']
Owner = _reflection.GeneratedProtocolMessageType('Owner', (_message.Message,), {
  'DESCRIPTOR' : _OWNER,
  '__module__' : 'owner_pb2'
  # @@protoc_insertion_point(class_scope:Owner)
  })
_sym_db.RegisterMessage(Owner)

OwnerContainer = _reflection.GeneratedProtocolMessageType('OwnerContainer', (_message.Message,), {
  'DESCRIPTOR' : _OWNERCONTAINER,
  '__module__' : 'owner_pb2'
  # @@protoc_insertion_point(class_scope:OwnerContainer)
  })
_sym_db.RegisterMessage(OwnerContainer)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _OWNER._serialized_start=15
  _OWNER._serialized_end=75
  _OWNERCONTAINER._serialized_start=77
  _OWNERCONTAINER._serialized_end=118
# @@protoc_insertion_point(module_scope)
