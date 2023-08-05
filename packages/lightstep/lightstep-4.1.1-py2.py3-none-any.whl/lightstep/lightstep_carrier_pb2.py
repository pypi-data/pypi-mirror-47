# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: lightstep_carrier.proto

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
  name='lightstep_carrier.proto',
  package='lightstep',
  syntax='proto3',
  serialized_pb=_b('\n\x17lightstep_carrier.proto\x12\tlightstep\"o\n\rBinaryCarrier\x12,\n\x08text_ctx\x18\x01 \x03(\x0b\x32\x1a.lightstep.TextCarrierPair\x12\x30\n\tbasic_ctx\x18\x02 \x01(\x0b\x32\x1d.lightstep.BasicTracerCarrier\"\xc5\x01\n\x12\x42\x61sicTracerCarrier\x12\x10\n\x08trace_id\x18\x01 \x01(\x06\x12\x0f\n\x07span_id\x18\x02 \x01(\x06\x12\x0f\n\x07sampled\x18\x03 \x01(\x08\x12\x46\n\rbaggage_items\x18\x04 \x03(\x0b\x32/.lightstep.BasicTracerCarrier.BaggageItemsEntry\x1a\x33\n\x11\x42\x61ggageItemsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"-\n\x0fTextCarrierPair\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\tb\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_BINARYCARRIER = _descriptor.Descriptor(
  name='BinaryCarrier',
  full_name='lightstep.BinaryCarrier',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='text_ctx', full_name='lightstep.BinaryCarrier.text_ctx', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='basic_ctx', full_name='lightstep.BinaryCarrier.basic_ctx', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=38,
  serialized_end=149,
)


_BASICTRACERCARRIER_BAGGAGEITEMSENTRY = _descriptor.Descriptor(
  name='BaggageItemsEntry',
  full_name='lightstep.BasicTracerCarrier.BaggageItemsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='lightstep.BasicTracerCarrier.BaggageItemsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='lightstep.BasicTracerCarrier.BaggageItemsEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001')),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=298,
  serialized_end=349,
)

_BASICTRACERCARRIER = _descriptor.Descriptor(
  name='BasicTracerCarrier',
  full_name='lightstep.BasicTracerCarrier',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='trace_id', full_name='lightstep.BasicTracerCarrier.trace_id', index=0,
      number=1, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='span_id', full_name='lightstep.BasicTracerCarrier.span_id', index=1,
      number=2, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sampled', full_name='lightstep.BasicTracerCarrier.sampled', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='baggage_items', full_name='lightstep.BasicTracerCarrier.baggage_items', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_BASICTRACERCARRIER_BAGGAGEITEMSENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=152,
  serialized_end=349,
)


_TEXTCARRIERPAIR = _descriptor.Descriptor(
  name='TextCarrierPair',
  full_name='lightstep.TextCarrierPair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='lightstep.TextCarrierPair.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='lightstep.TextCarrierPair.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=351,
  serialized_end=396,
)

_BINARYCARRIER.fields_by_name['text_ctx'].message_type = _TEXTCARRIERPAIR
_BINARYCARRIER.fields_by_name['basic_ctx'].message_type = _BASICTRACERCARRIER
_BASICTRACERCARRIER_BAGGAGEITEMSENTRY.containing_type = _BASICTRACERCARRIER
_BASICTRACERCARRIER.fields_by_name['baggage_items'].message_type = _BASICTRACERCARRIER_BAGGAGEITEMSENTRY
DESCRIPTOR.message_types_by_name['BinaryCarrier'] = _BINARYCARRIER
DESCRIPTOR.message_types_by_name['BasicTracerCarrier'] = _BASICTRACERCARRIER
DESCRIPTOR.message_types_by_name['TextCarrierPair'] = _TEXTCARRIERPAIR

BinaryCarrier = _reflection.GeneratedProtocolMessageType('BinaryCarrier', (_message.Message,), dict(
  DESCRIPTOR = _BINARYCARRIER,
  __module__ = 'lightstep_carrier_pb2'
  # @@protoc_insertion_point(class_scope:lightstep.BinaryCarrier)
  ))
_sym_db.RegisterMessage(BinaryCarrier)

BasicTracerCarrier = _reflection.GeneratedProtocolMessageType('BasicTracerCarrier', (_message.Message,), dict(

  BaggageItemsEntry = _reflection.GeneratedProtocolMessageType('BaggageItemsEntry', (_message.Message,), dict(
    DESCRIPTOR = _BASICTRACERCARRIER_BAGGAGEITEMSENTRY,
    __module__ = 'lightstep_carrier_pb2'
    # @@protoc_insertion_point(class_scope:lightstep.BasicTracerCarrier.BaggageItemsEntry)
    ))
  ,
  DESCRIPTOR = _BASICTRACERCARRIER,
  __module__ = 'lightstep_carrier_pb2'
  # @@protoc_insertion_point(class_scope:lightstep.BasicTracerCarrier)
  ))
_sym_db.RegisterMessage(BasicTracerCarrier)
_sym_db.RegisterMessage(BasicTracerCarrier.BaggageItemsEntry)

TextCarrierPair = _reflection.GeneratedProtocolMessageType('TextCarrierPair', (_message.Message,), dict(
  DESCRIPTOR = _TEXTCARRIERPAIR,
  __module__ = 'lightstep_carrier_pb2'
  # @@protoc_insertion_point(class_scope:lightstep.TextCarrierPair)
  ))
_sym_db.RegisterMessage(TextCarrierPair)


_BASICTRACERCARRIER_BAGGAGEITEMSENTRY.has_options = True
_BASICTRACERCARRIER_BAGGAGEITEMSENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001'))
# @@protoc_insertion_point(module_scope)
