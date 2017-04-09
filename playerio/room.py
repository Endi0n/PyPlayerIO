import socket
from .message import Message
from ._serializer import Serializer
from ._deserializer import Deserializer


class Room:

    def __init__(self, room_info):
        self.__event_handlers = {}

        endpoint = [x for x in room_info.endpoints if x.port == 8184][0]

        self.__socket = socket.create_connection((endpoint.address, endpoint.port))
        self.__socket.settimeout(10)

        self.__socket.send('\0'.encode())
        self.send('join', room_info.join_key)

        self.__deserializer = Deserializer(self.__socket, self.__broadcast_message)

    @property
    def connected(self):
        return self.__deserializer.connected

    def disconnect(self):
        self.__deserializer.disconnect()

    def send(self, message, *args):
        self.__socket.send(Serializer.serialize_message(
            message if type(message) == Message else Message(message, *args)))

    def add_handler(self, message_type):
        def event_handler(func):
            if message_type not in self.__event_handlers:
                self.__event_handlers[message_type] = []
            self.__event_handlers[message_type].append(func)
        return event_handler

    def __broadcast_message(self, message):
        if message.type == 'playerio.joinresult' and message[0]:
            self.__broadcast_message(Message('playerio.connect'))
        if message.type in self.__event_handlers:
            message_type_handlers = self.__event_handlers[message.type]
            for handler in message_type_handlers:
                handler(message)
