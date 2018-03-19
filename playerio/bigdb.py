from ._http_channel import HTTPChannel
from .databaseobject import DatabaseObject
from .playerio_pb2 import *

class BigDB:
    def __init__(self, channel:HTTPChannel):
        self.__channel = channel
        pass

    def load_my_playerobject(self):
        input_message = LoadMyPlayerObjectArgs()
        output_message = LoadMyPlayerObjectOutput()
        error_message = LoadMyPlayerObjectError()

        self.__channel.request(103, input_message, output_message, error_message)
        return DatabaseObject('PlayerObjects', output_message.playerObject.key, output_message.playerObject.properties, output_message.playerObject.version)

    def load(self, table, keys):
        input_message = LoadObjectsArgs()
        output_message = LoadObjectsOutput()
        error_message = LoadObjectsError()

        ids = BigDBObjectId()
        ids.table = table
        ids.keys.extend(keys)

        input_message.objectIds.extend([ids])

        self.__channel.request(85, input_message, output_message, error_message)
        return output_message.objects