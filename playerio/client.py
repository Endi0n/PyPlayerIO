from .room import Room
from ._http_channel import HTTPChannel
from ._bigdb import BigDBObject
from ._protocol_pb2 import *

class Client:

    def __init__(self, game_id, username_or_email, password):
        # Connecting
        self.__channel = HTTPChannel()

        # Initializing connection parameters
        input_message = SimpleConnectRequest()
        input_message.game_id = game_id
        input_message.username_or_email = username_or_email
        input_message.password = password
        input_message.client_api = 'PyPlayerIO'

        # Initializing request types
        output_message = SimpleConnectOutput()
        error_message = SimpleConnectError()

        # Sending the request
        self.__channel.request(400, input_message, output_message, error_message)

        # If authentication succeeds
        self.__channel.token = output_message.token
        self.__user_id = output_message.user_id

        # Load Player Object
        input_message = LoadMyPlayerObjectArgs()
        output_message = LoadMyPlayerObjectOutput()
        error_message = LoadMyPlayerObjectError()

        self.__channel.request(103, input_message, output_message, error_message)
        self.__player_object = BigDBObject.parse(output_message.player_object.items)

    def list_rooms(self, room_type, limit=0):
        # Initializing room-list parameters
        input_message = ListRoomsRequest()
        input_message.room_type = room_type
        input_message.limit = limit

        # Initializing request types
        output_message = ListRoomsOutput()
        error_message = ListRoomsError()

        # Sending the request
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

        # Sending the request
        self.__channel.request(27, input_message, output_message, error_message)

        # Initializing the room
        return Room(output_message)
    
    def bigdb_load(self, table, key):
        # Initializing BigDB load parameters
        input_message = BigDBLoadRequest()
        obj_id = BigDBObjectId()
        obj_id.table = table
        obj_id.keys.extend([key])
        input_message.object_ids.extend([obj_id])

        # Initializing request types
        output_message = BigDBLoadOutput()
        error_message = BigDBLoadError()

        # Sending the request
        self.__channel.request(85, input_message, output_message, error_message)

        # Returning the object assuming there's only one object with the specified key
        return BigDBObject.parse(output_message.objects[0].items)

    @property
    def user_id(self):
        return self.__user_id

    @property
    def player_object(self):
        return self.__player_object

    def __getitem__(self, key):
        return self.__player_object[key]
