from .room import Room
from .bigdb import BigDB
from ._http_channel import HTTPChannel
from .playerio_pb2 import *

class Client:

    def __init__(self, game_id, username_or_email, password):
        # Connecting
        self.__channel = HTTPChannel()
        self.BigDB = BigDB(self.__channel)

        # Initializing connection parameters
        input_message = SimpleConnectRequest()
        input_message.game_id = game_id
        input_message.username_or_email = username_or_email
        input_message.password = password
        input_message.client_api = 'PyPlayerIO'

        # Initializing request types
        output_message = SimpleConnectOutput()
        error_message = SimpleConnectError()

        self.__channel.request(400, input_message, output_message, error_message)

        # If authentication succeeds
        self.__channel.token = output_message.token
        self.__user_id = output_message.user_id

    def list_rooms(self, room_type, limit=0):
        # Initializing room-list parameters
        input_message = ListRoomsRequest()
        input_message.room_type = room_type
        input_message.limit = limit

        # Initializing request types
        output_message = ListRoomsOutput()
        error_message = ListRoomsError()

        self.__channel.request(30, input_message, output_message, error_message)

        # Return the results
        for room in output_message.rooms:
            yield room

    def create_join_room(self, room_id, room_type, visible, room_data={}):
        # Initializing create/join room parameters
        input_message = CreateJoinRoomRequest()
        input_message.room_id = room_id
        input_message.room_type = room_type
        input_message.visible = visible
        input_message.room_data.update(room_data)

        # Initializing request types
        output_message = CreateJoinRoomOutput()
        error_message = CreateJoinRoomError()

        self.__channel.request(27, input_message, output_message, error_message)

        # Initializing the room
        return Room(output_message)

    @property
    def user_id(self):
        return self.__user_id