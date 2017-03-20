from .protocol import *
from .http_channel import HTTPChannel
from .room import Room


class Client:

    def __init__(self, game_id, username_or_email, password):
        # This will probably serve later as identifiers
        self.__game_id = game_id
        self.__username_or_email = username_or_email

        # Connecting
        self.__channel = HTTPChannel()

        # Initializing connection parameters
        message_in = SimpleConnectRequest()
        message_in.game_id = game_id
        message_in.username_or_email = username_or_email
        message_in.password = password
        message_in.client_api = '<(^python^)>'  # this should be a smiley face

        # Initializing request types
        message_out = SimpleConnectOutput()
        message_error = SimpleConnectError()

        self.__channel.request(400, message_in, message_out, message_error)

        # If authentication fails the request raises an PlayerIOError and this breaks

        # If authentication succeeds
        self.__channel.token = message_out.token
        self.__user_id = message_out.user_id

    def list_rooms(self, room_type, limit=0):
        # Initializing room-list parameters
        message_in = ListRoomsRequest()
        message_in.room_type = room_type
        message_in.limit = limit

        # Initializing request types
        message_out = ListRoomsOutput()
        message_error = ListRoomsError()

        self.__channel.request(30, message_in, message_out, message_error)

        # Return the results
        for room in message_out.rooms:
            yield room

    def create_join_room(self, room_id, room_type, visible, room_data={}):
        # Initializing create/join room parameters
        message_in = CreateJoinRoomRequest()
        message_in.room_id = room_id
        message_in.room_type = room_type
        message_in.visible = visible
        message_in.room_data.update(room_data)

        # Initializing request types
        message_out = CreateJoinRoomOutput()
        message_error = CreateJoinRoomError()

        self.__channel.request(27, message_in, message_out, message_error)
        # If authentication fails the request raises an PlayerIOError and this breaks

        return Room(self, message_out)

    @property
    def user_id(self):
        return self.__user_id
