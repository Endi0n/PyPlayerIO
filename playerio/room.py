import socket
from .message import Message
from ._serializer import Serializer
from ._deserializer import Deserializer
from ._event_handler import EventHandler


class Room:

    def __init__(self, room_info):
        self.__room_id = room_info.id

        endpoint = [x for x in room_info.endpoints if x.port == 8184][0]

        self.__socket = socket.create_connection((endpoint.address, endpoint.port))
        self.__socket.settimeout(10)

        self.__socket.send('\0'.encode())
        self.send('join', room_info.join_key)

        self.__deserializer = Deserializer(self.__socket, self.__broadcast_message)

    @property
    def id(self):
        return self.__room_id

    @property
    def connected(self):
        return self.__deserializer.connected

    def disconnect(self):
        self.__deserializer.disconnect()

    def send(self, message, *args):
        self.__socket.send(Serializer.serialize_message(message if type(message) == Message else
                                                        Message(message, *args)))

    def __broadcast_message(self, message):
        if message.type == 'playerio.joinresult':
            return
        EventHandler.broadcast(self, message)
