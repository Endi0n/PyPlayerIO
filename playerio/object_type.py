from enum import Enum

class ObjectType(Enum):
        String = 0,
        Int = 1,
        UInt = 2,
        Long = 3,
        Bool = 4,
        Float = 5,
        Double = 6,
        ByteArray = 7,
        DateTime = 8,
        DatabaseArray = 9,
        DatabaseObject = 10