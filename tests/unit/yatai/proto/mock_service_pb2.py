# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mock_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='mock_service.proto',
  package='bentoml',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x12mock_service.proto\x12\x07\x62\x65ntoml\"\x1c\n\x0bMockRequest\x12\r\n\x05input\x18\x01 \x01(\t\"\x1e\n\x0cMockResponse\x12\x0e\n\x06output\x18\x01 \x01(\t2\x9f\x02\n\x0bMockService\x12\x36\n\x07\x45xecute\x12\x14.bentoml.MockRequest\x1a\x15.bentoml.MockResponse\x12\x44\n\x13\x45xecuteClientStream\x12\x14.bentoml.MockRequest\x1a\x15.bentoml.MockResponse(\x01\x12\x44\n\x13\x45xecuteServerStream\x12\x14.bentoml.MockRequest\x1a\x15.bentoml.MockResponse0\x01\x12L\n\x19\x45xecuteClientServerStream\x12\x14.bentoml.MockRequest\x1a\x15.bentoml.MockResponse(\x01\x30\x01\x62\x06proto3'
)




_MOCKREQUEST = _descriptor.Descriptor(
  name='MockRequest',
  full_name='bentoml.MockRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='input', full_name='bentoml.MockRequest.input', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=31,
  serialized_end=59,
)


_MOCKRESPONSE = _descriptor.Descriptor(
  name='MockResponse',
  full_name='bentoml.MockResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='output', full_name='bentoml.MockResponse.output', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=61,
  serialized_end=91,
)

DESCRIPTOR.message_types_by_name['MockRequest'] = _MOCKREQUEST
DESCRIPTOR.message_types_by_name['MockResponse'] = _MOCKRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MockRequest = _reflection.GeneratedProtocolMessageType('MockRequest', (_message.Message,), {
  'DESCRIPTOR' : _MOCKREQUEST,
  '__module__' : 'mock_service_pb2'
  # @@protoc_insertion_point(class_scope:bentoml.MockRequest)
  })
_sym_db.RegisterMessage(MockRequest)

MockResponse = _reflection.GeneratedProtocolMessageType('MockResponse', (_message.Message,), {
  'DESCRIPTOR' : _MOCKRESPONSE,
  '__module__' : 'mock_service_pb2'
  # @@protoc_insertion_point(class_scope:bentoml.MockResponse)
  })
_sym_db.RegisterMessage(MockResponse)



_MOCKSERVICE = _descriptor.ServiceDescriptor(
  name='MockService',
  full_name='bentoml.MockService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=94,
  serialized_end=381,
  methods=[
  _descriptor.MethodDescriptor(
    name='Execute',
    full_name='bentoml.MockService.Execute',
    index=0,
    containing_service=None,
    input_type=_MOCKREQUEST,
    output_type=_MOCKRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ExecuteClientStream',
    full_name='bentoml.MockService.ExecuteClientStream',
    index=1,
    containing_service=None,
    input_type=_MOCKREQUEST,
    output_type=_MOCKRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ExecuteServerStream',
    full_name='bentoml.MockService.ExecuteServerStream',
    index=2,
    containing_service=None,
    input_type=_MOCKREQUEST,
    output_type=_MOCKRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ExecuteClientServerStream',
    full_name='bentoml.MockService.ExecuteClientServerStream',
    index=3,
    containing_service=None,
    input_type=_MOCKREQUEST,
    output_type=_MOCKRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_MOCKSERVICE)

DESCRIPTOR.services_by_name['MockService'] = _MOCKSERVICE

# @@protoc_insertion_point(module_scope)