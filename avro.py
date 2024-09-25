from avro.datafile import DataFileWriter
from avro.io import DatumWriter
from avro.schema import Parse
from avro.datafile import DataFileReader
from avro.io import DatumReader

# Определение схемы Avro
schema = """
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "name", "type": "string"},
    {"name": "age", "type": "int"},
    {"name": "email", "type": "string"}
  ]
}
"""

# Создание объекта для сериализации
user = {"name": "John Doe", "age": 30, "email": "john.doe@example.com"}

# Сериализация объекта в файл Avro
with DataFileWriter(open("users.avro", "wb"), DatumWriter(), Parse(schema)) as writer:
    writer.append(user)

# Десериализация объекта из файла Avro
with DataFileReader(open("users.avro", "rb"), DatumReader()) as reader:
    for user in reader:
        print(user)

# Вывод:
# {'name': 'John Doe', 'age': 30, 'email': 'john.doe@example.com'}