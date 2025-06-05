import struct
from typing import Any

from .types import DataType, CompositeType


class ProtocolEncoder:
    @staticmethod
    def encode_type_byte(composite: CompositeType, primitive: DataType) -> int:
        return (composite << 4) | primitive

    @staticmethod
    def encode_value(value: Any) -> bytes:
        if isinstance(value, bool):
            return bytes([DataType.BOOL]) + bytes([int(value)])
        elif isinstance(value, int):
            return bytes([DataType.INT]) + struct.pack('<q', value)
        elif isinstance(value, float):
            return bytes([DataType.FLOAT]) + struct.pack('<d', value)
        elif isinstance(value, str):
            encoded_str = value.encode('utf-8')
            return (bytes([DataType.STRING]) +
                    struct.pack('<I', len(encoded_str)) +
                    encoded_str)
        elif isinstance(value, bytes):
            return (bytes([DataType.BLOB]) +
                    struct.pack('<I', len(value)) +
                    value)
        elif isinstance(value, (bytes, bytearray)):
            return (bytes([DataType.BLOB]) +
                    struct.pack('<I', len(value)) +
                    bytes(value))
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")

    @staticmethod
    def encode_composite_value(value: Any) -> bytes:
        if isinstance(value, (list, tuple)):
            return ProtocolEncoder.encode_array(value)
        elif isinstance(value, dict):
            return ProtocolEncoder.encode_map(value)
        else:
            return (bytes([CompositeType.PRIMITIVE]) +
                    ProtocolEncoder.encode_value(value))

    @staticmethod
    def encode_string(value: str) -> bytes:
        encoded = value.encode('utf-8')
        return struct.pack('<I', len(encoded)) + encoded

    @staticmethod
    def encode_length(length: int) -> bytes:
        return struct.pack('<I', length)

    @staticmethod
    def encode_array(array: list) -> bytes:
        result = bytes([CompositeType.ARRAY])
        result += struct.pack('<I', len(array))

        for item in array:
            result += ProtocolEncoder.encode_composite_value(item)

        return result

    @staticmethod
    def encode_map(map_dict: dict) -> bytes:
        result = bytes([CompositeType.MAP])
        result += struct.pack('<I', len(map_dict))

        for key, value in map_dict.items():
            result += ProtocolEncoder.encode_composite_value(key)
            result += ProtocolEncoder.encode_composite_value(value)

        return result
