# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: embedding.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'embedding.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0f\x65mbedding.proto\"\x80\x01\n\x14\x45mbeddingUserRequest\x12\r\n\x05\x64type\x18\x01 \x01(\t\x12\x0c\n\x04size\x18\x02 \x01(\x05\x12\r\n\x05\x65mail\x18\x03 \x01(\t\x12\x10\n\x08nickname\x18\x04 \x01(\t\x12\x10\n\x08\x66\x61vorite\x18\x05 \x01(\t\x12\x0b\n\x03lat\x18\x06 \x01(\x02\x12\x0b\n\x03lng\x18\x07 \x01(\x02\"(\n\x15\x45mbeddingUserResponse\x12\x0f\n\x07\x62vector\x18\x01 \x01(\x0c\x32R\n\x10\x45mbeddingService\x12>\n\rEmbeddingUser\x12\x15.EmbeddingUserRequest\x1a\x16.EmbeddingUserResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'embedding_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_EMBEDDINGUSERREQUEST']._serialized_start=20
  _globals['_EMBEDDINGUSERREQUEST']._serialized_end=148
  _globals['_EMBEDDINGUSERRESPONSE']._serialized_start=150
  _globals['_EMBEDDINGUSERRESPONSE']._serialized_end=190
  _globals['_EMBEDDINGSERVICE']._serialized_start=192
  _globals['_EMBEDDINGSERVICE']._serialized_end=274
# @@protoc_insertion_point(module_scope)
