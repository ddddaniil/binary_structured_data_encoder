import struct


class SimpleObjectSerializer:

    def __init__(self):
        self.types = {
            int: self._encode_int,
            float: self._encode_float,
            str: self._encode_str,
            bool: self._encode_bool,
            list: self._encode_list,
            dict: self._encode_dict,
        }

    def serialize(self, obj):
        return self._encode(obj)

    def deserialize(self, data):
        return self._decode(data)

    def _encode(self, obj):
        if isinstance(obj, type(None)):
            return b'\x00'
        data_type = type(obj)
        encoder = self.types.get(data_type)
        if encoder:
            return encoder(obj)
        else:
            raise TypeError(f"Unsupported type: {data_type}")

    def _decode(self, data):
        if data == b'\x00':
            return None

        if not data:
            return None, data

        data_type = data[0]
        if data_type == 0:
            return self._decode_int(data[1:])
        elif data_type == 1:
            return self._decode_float(data[1:])
        elif data_type == 2:
            return self._decode_str(data[1:])
        elif data_type == 3:
            return self._decode_bool(data[1:])
        elif data_type == 4:
            return self._decode_list(data[1:])
        elif data_type == 5:
            return self._decode_dict(data[1:])
        else:
            raise ValueError(f"Unknown data type: {data_type}")

    def _encode_int(self, obj):
        #encoded_int = obj.to_bytes((obj.bit_length() + 7) // 8, 'big')
        encoded_int = obj.to_bytes(4, byteorder='big')
        return b'\x00' + encoded_int

    def _encode_float(self, obj):
        encoded_float = struct.pack('>f', obj)
        return b'\x01' + encoded_float

    def _encode_str(self, obj):
        encoded_str = obj.encode('utf-8')
        return b'\x02' + len(encoded_str).to_bytes(4, 'big') + encoded_str

    def _encode_bool(selfself, obj):
        encoded_bool = (b'\x01' if obj else b'\x00')
        return b'\x03' + encoded_bool

    def _encode_list(self, obj):
        encoded_list = b''
        for item in obj:
            encoded_list += self._encode(item)
        return b'\x04' + len(encoded_list).to_bytes(4, 'big') + encoded_list

    def _encode_dict(self, obj):
        encoded_dict = b''
        for key, value in obj.items():
            encoded_dict += self._encode(key) + self._encode(value)
        return b'\x05' + len(encoded_dict).to_bytes(4, 'big') + encoded_dict

    def _decode_int(self, data):
        return int.from_bytes(data, 'big')

    def _decode_float(self, data):
        return struct.unpack('>f', data[:4])[0]

    def _decode_str(self, data):
        length = int.from_bytes(data[:4], 'big')
        return data[4:4 + length].decode('utf-8')

    def _decode_bool(self, data):
        return bool(data[0])

    def _decode_list(self, data):
        length = int.from_bytes(data[:4], 'big')
        decoded_list = []
        offset = 4
        while offset < length + 4:
            decoded_item = self._decode(data[offset:])
            decoded_list.append(decoded_item)
            offset += len(self._encode(decoded_item))
        return decoded_list

    def _decode_dict(self, data):
        length = int.from_bytes(data[:4], 'big')
        decoded_dict = {}
        offset = 4
        while offset < length + 4:
            key = self._decode(data[offset:])
            offset += len(self._encode(key))
            value = self._decode(data[offset:])
            offset += len(self._encode(value))
            decoded_dict[key] = value
        return decoded_dict


#obj = {'a': '1', 'b': {'1': 'a'}, 'c': '2', 'd': 2.202}
#obj = {'a': '1', 'b': '2', 'c': {'d': '3'}}
obj = {
    "name": "John Doe",
    "age": 30.0,
    "is_active": True,
    "hobbies": ["reading", "coding"]
}

ser = SimpleObjectSerializer().serialize(obj)
des = SimpleObjectSerializer().deserialize(ser)
# enc = SimpleObjectSerializer()._encode_list(obj)
# dec = SimpleObjectSerializer()._decode(enc)

print(ser, des, sep='\n')
# print(enc)
