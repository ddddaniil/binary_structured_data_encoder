import time
import struct

# Тестовый объект
obj = {
    "name": "John",
    "age": 30,
    "is_student": False,
    "friends": [
        {"name": "Jane", "age": 25},
        {"name": "Mike", "age": 32}
    ]
}

from test import *
# Замеры времени кодирования/декодирования для своего формата
start_time = time.time()
encoded_data_custom = serialize(obj)
end_time = time.time()
encode_time_custom = end_time - start_time

start_time = time.time()
decoded_obj_custom = deserialize(encoded_data_custom)
end_time = time.time()
decode_time_custom = end_time - start_time

# Используем библиотеку protobuf
import OpenAI.protobuf.message as message
from OpenAI.protobuf import descriptor
from OpenAI.protobuf import text_format
from OpenAI.protobuf import json_format

# Определяем схему protobuf
schema = """
message Person {
  string name = 1;
  int32 age = 2;
  bool is_student = 3;
}

message Friend {
  Person person = 1;
}

message User {
  string name = 1;
  int32 age = 2;
  bool is_student = 3;
  repeated Friend friends = 4;
}
"""

# Создаем объект protobuf
descriptor = descriptor.FileDescriptor.FromString(schema.encode())
User_pb = descriptor.message_types_by_name['User']
user_pb = message.Message()
user_pb.__class__ = User_pb
user_pb.name = obj['name']
user_pb.age = obj['age']
user_pb.is_student = obj['is_student']
for friend in obj['friends']:
    friend_pb = message.Message()
    friend_pb.__class__ = descriptor.message_types_by_name['Friend']
    person_pb = message.Message()
    person_pb.__class__ = descriptor.message_types_by_name['Person']
    person_pb.name = friend['name']
    person_pb.age = friend['age']
    friend_pb.person = person_pb
    user_pb.friends.append(friend_pb)

# Замеры времени кодирования/декодирования
start_time = time.time()
encoded_data_protobuf = user_pb.SerializeToString()
end_time = time.time()
encode_time_protobuf = end_time - start_time

start_time = time.time()
decoded_obj_protobuf = User_pb()
decoded_obj_protobuf.ParseFromString(encoded_data_protobuf)
end_time = time.time()
decode_time_protobuf = end_time - start_time

# Используем библиотеку avro
from avro.schema import Parse
from avro.io import DatumWriter, BinaryEncoder
from avro.datafile import DataFileWriter

# Определяем схему avro
schema = """
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "name", "type": "string"},
    {"name": "age", "type": "int"},
    {"name": "is_student", "type": "boolean"},
    {
      "name": "friends",
      "type": {
        "type": "array",
        "items": {
          "type": "record",
          "name": "Friend",
          "fields": [
            {
              "name": "person",
              "type": {
                "type": "record",
                "name": "Person",
                "fields": [
                  {"name": "name", "type": "string"},
                  {"name": "age", "type": "int"}
                ]
              }
            }
          ]
        }
      }
    }
  ]
}
"""

# Замеры времени кодирования/декодирования
start_time = time.time()
writer = DataFileWriter(open('user.avro', 'wb'), DatumWriter(), BinaryEncoder())
writer.append(obj)
writer.close()
end_time = time.time()
encode_time_avro = end_time - start_time

start_time = time.time()
with open('user.avro', 'rb') as f:
    reader = DataFileReader(f, DatumReader())
    decoded_obj_avro = reader.next()
    reader.close()
end_time = time.time()
decode_time_avro = end_time - start_time

# Вывод результатов
print("-" * 30)
print("Результаты сравнения:")
print("-" * 30)
print(f"Размер данных (custom): {len(encoded_data_custom)} байт")
print(f"Размер данных (protobuf): {len(encoded_data_protobuf)} байт")
print(f"Размер данных (avro): {len(open('user.avro', 'rb').read())} байт")
print(f"Время кодирования (custom): {encode_time_custom:.6f} сек")
print(f"Время кодирования (protobuf): {encode_time_protobuf:.6f} сек")
print(f"Время кодирования (avro): {encode_time_avro:.6f} сек")
print(f"Время декодирования (custom): {decode_time_custom:.6f} сек")
print(f"Время декодирования (protobuf): {decode_time_protobuf:.6f} сек")
print(f"Время декодирования (avro): {decode_time_avro:.6f} сек")