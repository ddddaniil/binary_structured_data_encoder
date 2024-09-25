n = 1

types = {
            int: 'self._encode_int',
            float: 'self._encode_float',
            str: 'self._encode_str',
            list: 'self._encode_list',
            dict: 'self._encode_dict',
        }

n_type = type(n)
encoder = types.get(n_type)

print(encoder)

from BSDE import SimpleObjectSerializer

obj = ['1','2','3']

ser = SimpleObjectSerializer().serialize(obj)
des = SimpleObjectSerializer().deserialize(ser)

print(ser, des, sep='\n')

object1 = {}
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

for _ in range(10000):
    key = str(n)
    n += 1
    object1[key] = value

print(object1)