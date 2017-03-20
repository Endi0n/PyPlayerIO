import socket
from threading import Thread
from .serializer import Serializer
from .deserializer import Deserializer
from .message import Message


class Room:

    def __init__(self, client, room_info):
        self.__client = client
        self.__info = room_info

        self.__event_handlers = {}
        self.__disconnect_handlers = []

        endpoint = [x for x in room_info.endpoints if x.port == 8184][0]

        self.__socket = socket.create_connection((endpoint.address, endpoint.port))
        self.__socket.settimeout(10)

        self.__socket.send('\0'.encode())
        self.send('join', room_info.join_key)

        self.__connected = True

        self.__deserializer = Deserializer()
        self.__deserializer.message_handler = self.__broadcast_message

        self.__thread = Thread(target=self.__read_socket_data)
        self.__thread.start()

    @property
    def connected(self):
        return self.__connected

    def send(self, message_type, *args):
        self.send_message(Message(message_type, *args))

    def send_message(self, message):
        self.__socket.send(Serializer.serialize_message(message))

    def __read_socket_data(self):
        while self.__connected:
            self.__deserializer.queue(self.__socket.recv(4096))

    def add_event_handler(self, message_type):
        def event_handler(func):
            if message_type not in self.__event_handlers:
                self.__event_handlers[message_type] = []
            self.__event_handlers[message_type].append(func)
        return event_handler

    def __broadcast_message(self, message):
        if message.type in self.__event_handlers:
            message_type_handlers = self.__event_handlers[message.type]
            for handler in message_type_handlers:
                handler(message)
