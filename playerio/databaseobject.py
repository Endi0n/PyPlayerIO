from .playerio_pb2 import *
from .object_type import ObjectType

class DatabaseObject:
    def __init__(self, table, key, properties, version):
        self.__table = table
        self.__key = key
        self.__properties = properties
        self.__version = version

        #self.properties = self.convert_to_dictionary(self)

    # todo: fix this
    def convert_to_dictionary(self, input):
        dictionary = dict()

        if (isinstance(input, DatabaseObject)):
            for property in input.__properties:
                dictionary[property.name] = self.convert_to_dictionary(property.value)
        elif (isinstance(input, ValueObject)):
            if (input.valueType == ObjectType.DatabaseObject or input.valueType == ObjectType.DatabaseArray):
                for property in input.value:
                    dictionary[property.name] = self.convert_to_dictionary(property.value)
            else: return self.convert_to_dictionary(input.ListFields()[1][1]) # should always be one value field!
        else: return input

        return dictionary