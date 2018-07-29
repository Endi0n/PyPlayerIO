from io import BytesIO


class Serializer:

    PATTERNS = {
        'false': 0x00,
        'true': 0x01,
        'float': 0x02,
        'double': 0x03,
        'int': 0x04,
        'unsigned_int': 0x08,
        'byte_array': 0x10,
        'string': 0x0C,
        'short_long': 0x30,
        'long': 0x34,
        'unsigned_short_long': 0x38,
        'unsigned_long': 0x3C,
        'short_byte_array': 0x40,
        'unsigned_short_int': 0x80,
        'short_string': 0xC0
    }

    def __init__(self):
        raise NotImplementedError('Serializer is a static class!')

    @staticmethod
    def serialize_message(message):
        buffer = BytesIO()
        buffer.write(Serializer.serialize_value(len(message)))
        buffer.write(Serializer.serialize_value(message.type))
        for value in message:
            buffer.write(Serializer.serialize_value(value))
        return buffer.getvalue()

    @staticmethod
    def serialize_value(value):
        value_type = type(value)

        if value_type == bool:
            return bytes([Serializer.PATTERNS['true'] if value else Serializer.PATTERNS['false']])

        if value_type == int:
            if 0 <= value < 64:
                return bytes([Serializer.PATTERNS['unsigned_short_int'] | value])
            return Serializer.__get_header(Serializer.PATTERNS['int'], value)

        if value_type == str:
            encoded_value = value.encode()
            if len(encoded_value) < 64:
                return bytes([Serializer.PATTERNS['short_string'] | len(encoded_value)]) + encoded_value
            return Serializer.__get_header(Serializer.PATTERNS['string'], len(encoded_value)) + encoded_value

        raise NotImplementedError('Value type {} is not implemented yet'.format(value_type))

    @staticmethod
    def __get_header(value_type, value):
        encoded_value = Serializer.__encode_value(value)
        return bytes([value_type | (len(encoded_value) - 1)]) + encoded_value

    @staticmethod
    def __encode_value(value):
        encode = b''
        while True:
            encode += bytes([value & 0xFF])
            value >>= 8
            if value == 0:
                break
        return encode[:: -1]
