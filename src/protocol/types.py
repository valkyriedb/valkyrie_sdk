from enum import IntEnum


class DataType(IntEnum):
    BOOL = 0
    INT = 1
    FLOAT = 2
    STRING = 3
    BLOB = 4


class CompositeType(IntEnum):
    PRIMITIVE = 0
    ARRAY = 1
    MAP = 2


class Operation(IntEnum):
    GET = 0
    SET = 1
    REMOVE = 2
    LEN = 3
    APPEND = 4
    INCREMENT = 5
    DECREMENT = 6

    INSERT = 7
    ARRAY_REMOVE = 8
    SLICE = 9

    MAP_GET = 0
    MAP_SET = 1
    MAP_REMOVE = 2
    MAP_CONTAINS = 10
    MAP_KEYS = 11
    MAP_VALUES = 12


class Status(IntEnum):
    OK = 0
    INVALID_REQUEST = 64
    UNAVAILABLE_OPERATION = 65
    UNAUTHORIZED = 69
    NOT_FOUND = 128
    WRONG_TYPE = 129
    OUT_OF_RANGE = 130
    INTERNAL_ERROR = 255