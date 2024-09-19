import struct


def serialize(obj):
    """Сериализует объект в байты."""

    def _encode(data):
        """Вспомогательная функция для кодирования."""
        if isinstance(data, int):
            return b'\x00' + data.to_bytes(4, byteorder='big')

        elif isinstance(data, float):
            return b'\x01' + struct.pack('>f', data)

        elif isinstance(data, str):
            encoded_str = data.encode('utf-8')
            return b'\x02' + len(encoded_str).to_bytes(4, byteorder='big') + encoded_str

        elif isinstance(data, bool):
            return b'\x03' + (b'\x01' if data else b'\x00')

        elif isinstance(data, list):
            encoded_list = b'\x04' + len(data).to_bytes(4, byteorder='big')
            for item in data:
                encoded_list += _encode(item)
            return encoded_list

        elif isinstance(data, dict):
            encoded_dict = b'\x05' + len(data).to_bytes(4, byteorder='big')
            for key, value in data.items():
                encoded_dict += _encode(key) + _encode(value)
            return encoded_dict

        elif data is None:
            return b'\x06'

        else:
            raise TypeError(f"Unsupported type: {type(data)}")

    encoded_obj = _encode(obj)
    return len(encoded_obj).to_bytes(4, byteorder='big') + encoded_obj


def deserialize(obj):
    """Десериализует байты в объект."""

    def _decode(bytes_data):
        """Вспомогательная функция для декодирования."""
        data_type = bytes_data[0]
        bytes_data = bytes_data[1:]

        if data_type == 0:
            return int.from_bytes(bytes_data[:4], byteorder='big')

        elif data_type == 1:
            return struct.unpack('>f', bytes_data[:4])[0]

        elif data_type == 2:
            str_len = int.from_bytes(bytes_data[:4], byteorder='big')
            return bytes_data[4:4+str_len].decode('utf-8')

        elif data_type == 3:
            return bool(bytes_data[0])

        elif data_type == 4:
            list_len = int.from_bytes(bytes_data[:4], byteorder='big')
            decoded_list = []
            bytes_data = bytes_data[4:]
            for _ in range(list_len):
                decoded_item = _decode(bytes_data)
                # Если _decode возвращает два значения, распаковываем их
                if isinstance(decoded_item, tuple):
                    decoded_item, bytes_data = decoded_item
                    bytes_data = decoded_item[1]
                decoded_list.append(decoded_item)
            return decoded_list, bytes_data

        elif data_type == 5:
            dict_len = int.from_bytes(bytes_data[:4], byteorder='big')
            decoded_dict = {}
            bytes_data = bytes_data[4:]
            for _ in range(dict_len):
                # Декодируем ключ
                key, bytes_data = _decode(bytes_data)  # Возвращает 2 значения (ключ и остаток байтов)
                # Декодируем значение
                value = _decode(bytes_data)  # Возвращает 1 значение (значение)

                # Если _decode возвращает 2 значения, обновляем bytes_data
                if isinstance(value, tuple):
                    value, bytes_data = value

                decoded_dict[key] = value
            return decoded_dict, bytes_data

        elif data_type == 6:
            return None, bytes_data

        else:
            raise TypeError(f"Unsupported data type: {data_type}")

    obj_len = int.from_bytes(obj[:4], byteorder='big')
    obj = _decode(obj[4:])
    return obj_len, obj


obj = [1,2,3]

print(serialize(obj))
print(deserialize(serialize(obj)))