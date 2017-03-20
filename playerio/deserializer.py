from io import BytesIO
import struct
from .message import Message
from .serializer import Serializer


class Deserializer:

    __STATE = {
        'init': 0,
        'header': 1,
        'data': 2
    }

    def __init__(self):
        self.message_handler = None
        self.__message = None
        self.__buffer = BytesIO()
        self.__state = self.__STATE['init']

        self.__value_type = None
        self.__value_length = None
        self.__message_length = None

    def queue(self, data):
        for byte in data:
            self.__parse(byte)

    def __parse(self, byte):
        if self.__state == self.__STATE['init']:
            self.__value_type = None
            for pattern in sorted(Serializer.PATTERNS.values(), reverse=True):
                if byte & pattern == pattern:
                    self.__value_type = pattern
                    break
            if self.__value_type is None:
                raise ValueError('Unknown value type for {}'.format(byte))

            if self.__value_type == Serializer.PATTERNS['false']:
                self.__add_value(False)
            elif self.__value_type == Serializer.PATTERNS['true']:
                self.__add_value(True)
            elif self.__value_type == Serializer.PATTERNS['float']:
                self.__value_length = 4
                self.__state = self.__STATE['data']
            elif self.__value_type == Serializer.PATTERNS['double']:
                self.__value_length = 8
                self.__state = self.__STATE['data']
            elif self.__value_type == Serializer.PATTERNS['int'] \
                    or self.__value_type == Serializer.PATTERNS['unsigned_int']:
                self.__value_length = (byte & ~self.__value_type) + 1
                self.__state = self.__STATE['data']
            elif self.__value_type == Serializer.PATTERNS['byte_array'] \
                    or self.__value_type == Serializer.PATTERNS['string']:
                self.__value_length = (byte & ~self.__value_type) + 1
                self.__state = self.__STATE['header']
            elif self.__value_type == Serializer.PATTERNS['short_long'] \
                    or self.__value_type == Serializer.PATTERNS['unsigned_short_long']:
                self.__value_length = 4
                self.__state = self.__STATE['data']
            elif self.__value_type == Serializer.PATTERNS['long'] \
                    or self.__value_type == Serializer.PATTERNS['unsigned_long']:
                self.__value_length = 6
                self.__state = self.__STATE['data']
            elif self.__value_type == Serializer.PATTERNS['short_byte_array']:
                self.__value_length = byte & ~self.__value_type
                if self.__value_length > 0:
                    self.__state = self.__STATE['data']
                else:
                    self.__add_value([])
            elif self.__value_type == Serializer.PATTERNS['unsigned_short_int']:
                self.__add_value(byte & ~self.__value_type)
            elif self.__value_type == Serializer.PATTERNS['short_string']:
                self.__value_length = byte & ~self.__value_type
                if self.__value_length > 0:
                    self.__state = self.__STATE['data']
                else:
                    self.__add_value('')
        elif self.__state == self.__STATE['header']:
            self.__buffer.write(bytes([byte]))
            if self.__buffer.tell() == self.__value_length:
                self.__value_length = self.__decode_value(self.__buffer.getvalue())
                self.__state = self.__STATE['data']
                self.__clear_buffer()
        elif self.__state == self.__STATE['data']:
            self.__buffer.write(bytes([byte]))
            if self.__buffer.tell() == self.__value_length:
                if self.__value_type == Serializer.PATTERNS['float']:
                    self.__add_value(struct.unpack('>f', self.__buffer.getvalue())[0])
                elif self.__value_type == Serializer.PATTERNS['double']:
                    self.__add_value(struct.unpack('>d', self.__buffer.getvalue())[0])
                elif self.__value_type == Serializer.PATTERNS['int']:
                    if self.__value_length == 4:
                        self.__add_value(struct.unpack('>i', self.__buffer.getvalue())[0])
                    else:
                        self.__add_value(self.__decode_value(self.__buffer.getvalue()))
                elif self.__value_type == Serializer.PATTERNS['unsigned_int']:
                    self.__add_value(self.__decode_value(self.__buffer.getvalue()))
                elif self.__value_type == Serializer.PATTERNS['byte_array'] \
                        or self.__value_type == Serializer.PATTERNS['short_byte_array']:
                    self.__add_value(self.__buffer.getvalue())
                elif self.__value_type == Serializer.PATTERNS['string'] \
                        or self.__value_type == Serializer.PATTERNS['short_string']:
                    self.__add_value(self.__buffer.getvalue().decode())
                elif self.__value_type == Serializer.PATTERNS['short_long'] \
                        or self.__value_type == Serializer.PATTERNS['long']:
                    self.__add_value(struct.unpack('>l', self.__buffer.getvalue())[0])
                elif self.__value_type == Serializer.PATTERNS['unsigned_short_long'] \
                        or self.__value_type == Serializer.PATTERNS['unsigned_long']:
                    self.__add_value(struct.unpack('>L', self.__buffer.getvalue())[0])

    @staticmethod
    def __decode_value(value):
        result = 0
        for byte in value:
            result <<= 8
            result |= byte & 0xFF
        return result

    def __add_value(self, value):
        message_done = False

        if self.__message_length is None:
            self.__message_length = value

        elif self.__message is None:
            self.__message = Message(value)
            if self.__message_length == 0:
                message_done = True

        else:
            self.__message_length -= 1
            if self.__message_length == 0:
                message_done = True
            self.__message.extend(value)

        if message_done:
            print(self.__message)
            if self.message_handler is not None:
                self.message_handler(self.__message)
            self.__message = None
            self.__message_length = None

        self.__state = self.__STATE['init']
        self.__clear_buffer()

    def __clear_buffer(self):
        if self.__buffer.tell() > 0:
            self.__buffer = BytesIO()
