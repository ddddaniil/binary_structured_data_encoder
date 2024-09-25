import time
from BSDE import SimpleObjectSerializer

# Тестовый объект
object = {}
n = 0
value = {
    "name": "John",
    "age": 30.0,
    "is_student": False,
    "friends": [
        {"name": "Jane", "age": 25.0},
        {"name": "Mike", "age": 32.0}
    ]
}

for _ in range(1000):
    key = str(n)
    n += 1
    object[key] = value


# Замеры времени кодирования/декодирования для своего формата
start_time = time.time()
ser = SimpleObjectSerializer().serialize(object)
end_time = time.time()
encode_time_custom = end_time - start_time

start_time = time.time()
des = SimpleObjectSerializer().deserialize(ser)
end_time = time.time()
decode_time_custom = end_time - start_time


# Вывод результатов
print("-" * 30)
print("Результаты сравнения:")
print("-" * 30)
print(f"Размер данных (custom): {len(ser)} байт")
print(f"Время кодирования (custom): {encode_time_custom:.20f} сек")
print(f"Время декодирования (custom): {decode_time_custom:.20f} сек")


