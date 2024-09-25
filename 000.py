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