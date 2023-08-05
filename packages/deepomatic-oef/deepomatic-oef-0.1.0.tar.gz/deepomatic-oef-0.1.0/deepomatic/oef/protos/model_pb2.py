# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: deepomatic/oef/protos/model.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from deepomatic.oef.protos.models import image_pb2 as deepomatic_dot_oef_dot_protos_dot_models_dot_image__pb2
from deepomatic.oef.protos import preprocessor_pb2 as deepomatic_dot_oef_dot_protos_dot_preprocessor__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='deepomatic/oef/protos/model.proto',
  package='deepomatic.oef.model',
  syntax='proto2',
  serialized_pb=_b('\n!deepomatic/oef/protos/model.proto\x12\x14\x64\x65\x65pomatic.oef.model\x1a(deepomatic/oef/protos/models/image.proto\x1a(deepomatic/oef/protos/preprocessor.proto\"Y\n\x0cQuantization\x12\x15\n\x05\x64\x65lay\x18\x01 \x01(\x05:\x06\x35\x30\x30\x30\x30\x30\x12\x16\n\x0bweight_bits\x18\x02 \x01(\x05:\x01\x38\x12\x1a\n\x0f\x61\x63tivation_bits\x18\x03 \x01(\x05:\x01\x38\"\xec\x04\n\x05Model\x12\x1c\n\x12pretrained_weights\x18\x01 \x01(\t:\x00\x12\x12\n\nbatch_size\x18\x02 \x02(\x05\x12\x1a\n\x0f\x65val_batch_size\x18\x03 \x01(\x05:\x01\x30\x12%\n\x17\x61\x64\x64_regularization_loss\x18\x04 \x01(\x08:\x04true\x12%\n\x19gradient_clipping_by_norm\x18\x05 \x01(\x02:\x02\x31\x30\x12!\n\x12use_moving_average\x18\x06 \x01(\x08:\x05\x66\x61lse\x12$\n\x14moving_average_decay\x18\x07 \x01(\x02:\x06\x30.9999\x12\x38\n\x0cquantization\x18\x08 \x01(\x0b\x32\".deepomatic.oef.model.Quantization\x12\x18\n\x10\x66reeze_variables\x18\t \x03(\t\x12\"\n\x1aupdate_trainable_variables\x18\n \x03(\t\x12Q\n\x19\x64\x61ta_augmentation_options\x18\x0b \x03(\x0b\x32..deepomatic.oef.preprocessor.PreprocessingStep\x12\x15\n\rlearning_rate\x18\x0c \x02(\x02\x12K\n\x14image_classification\x18@ \x01(\x0b\x32+.deepomatic.oef.models.image.ClassificationH\x00\x12\x41\n\x0fimage_detection\x18\x41 \x01(\x0b\x32&.deepomatic.oef.models.image.DetectionH\x00\x42\x0c\n\nmodel_type')
  ,
  dependencies=[deepomatic_dot_oef_dot_protos_dot_models_dot_image__pb2.DESCRIPTOR,deepomatic_dot_oef_dot_protos_dot_preprocessor__pb2.DESCRIPTOR,])




_QUANTIZATION = _descriptor.Descriptor(
  name='Quantization',
  full_name='deepomatic.oef.model.Quantization',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='delay', full_name='deepomatic.oef.model.Quantization.delay', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=500000,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='weight_bits', full_name='deepomatic.oef.model.Quantization.weight_bits', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=8,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='activation_bits', full_name='deepomatic.oef.model.Quantization.activation_bits', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=8,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=143,
  serialized_end=232,
)


_MODEL = _descriptor.Descriptor(
  name='Model',
  full_name='deepomatic.oef.model.Model',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pretrained_weights', full_name='deepomatic.oef.model.Model.pretrained_weights', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='batch_size', full_name='deepomatic.oef.model.Model.batch_size', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='eval_batch_size', full_name='deepomatic.oef.model.Model.eval_batch_size', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='add_regularization_loss', full_name='deepomatic.oef.model.Model.add_regularization_loss', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gradient_clipping_by_norm', full_name='deepomatic.oef.model.Model.gradient_clipping_by_norm', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(10),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='use_moving_average', full_name='deepomatic.oef.model.Model.use_moving_average', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='moving_average_decay', full_name='deepomatic.oef.model.Model.moving_average_decay', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.9999),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='quantization', full_name='deepomatic.oef.model.Model.quantization', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='freeze_variables', full_name='deepomatic.oef.model.Model.freeze_variables', index=8,
      number=9, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='update_trainable_variables', full_name='deepomatic.oef.model.Model.update_trainable_variables', index=9,
      number=10, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data_augmentation_options', full_name='deepomatic.oef.model.Model.data_augmentation_options', index=10,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='learning_rate', full_name='deepomatic.oef.model.Model.learning_rate', index=11,
      number=12, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='image_classification', full_name='deepomatic.oef.model.Model.image_classification', index=12,
      number=64, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='image_detection', full_name='deepomatic.oef.model.Model.image_detection', index=13,
      number=65, type=11, cpp_type=10, label=1,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='model_type', full_name='deepomatic.oef.model.Model.model_type',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=235,
  serialized_end=855,
)

_MODEL.fields_by_name['quantization'].message_type = _QUANTIZATION
_MODEL.fields_by_name['data_augmentation_options'].message_type = deepomatic_dot_oef_dot_protos_dot_preprocessor__pb2._PREPROCESSINGSTEP
_MODEL.fields_by_name['image_classification'].message_type = deepomatic_dot_oef_dot_protos_dot_models_dot_image__pb2._CLASSIFICATION
_MODEL.fields_by_name['image_detection'].message_type = deepomatic_dot_oef_dot_protos_dot_models_dot_image__pb2._DETECTION
_MODEL.oneofs_by_name['model_type'].fields.append(
  _MODEL.fields_by_name['image_classification'])
_MODEL.fields_by_name['image_classification'].containing_oneof = _MODEL.oneofs_by_name['model_type']
_MODEL.oneofs_by_name['model_type'].fields.append(
  _MODEL.fields_by_name['image_detection'])
_MODEL.fields_by_name['image_detection'].containing_oneof = _MODEL.oneofs_by_name['model_type']
DESCRIPTOR.message_types_by_name['Quantization'] = _QUANTIZATION
DESCRIPTOR.message_types_by_name['Model'] = _MODEL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Quantization = _reflection.GeneratedProtocolMessageType('Quantization', (_message.Message,), dict(
  DESCRIPTOR = _QUANTIZATION,
  __module__ = 'deepomatic.oef.protos.model_pb2'
  # @@protoc_insertion_point(class_scope:deepomatic.oef.model.Quantization)
  ))
_sym_db.RegisterMessage(Quantization)

Model = _reflection.GeneratedProtocolMessageType('Model', (_message.Message,), dict(
  DESCRIPTOR = _MODEL,
  __module__ = 'deepomatic.oef.protos.model_pb2'
  # @@protoc_insertion_point(class_scope:deepomatic.oef.model.Model)
  ))
_sym_db.RegisterMessage(Model)


# @@protoc_insertion_point(module_scope)
