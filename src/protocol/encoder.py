import struct
from typing import Any, Tuple
from .types import DataType, CompositeType


class ProtocolEncoder:
    @staticmethod
    def encode_type_byte(composite: CompositeType, primitive: DataType) -> int:
        return (composite << 4) | primitive

    @staticmethod
    def encode_value(value: Any) -> Tuple[bytes, DataType]:
        if isinstance(value, bool):
            return struct.pack('<B', 1 if value else 0), DataType.BOOL
        elif isinstance(value, int):
            return struct.pack('<q', value), DataType.INT
        elif isinstance(value, float):
            return struct.pack('<d', value), DataType.FLOAT
        elif isinstance(value, str):
            encoded = value.encode('utf-8')
            return struct.pack('<I', len(encoded)) + encoded, DataType.STRING
        elif isinstance(value, (bytes, bytearray)):
            return struct.pack('<I', len(value)) + value, DataType.BLOB
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")

    @staticmethod
    def encode_string(value: str) -> bytes:
        """Encode a string with length prefix"""
        encoded = value.encode('utf-8')
        return struct.pack('<I', len(encoded)) + encoded

    @staticmethod
    def encode_length(length: int) -> bytes:
        """Encode a 32-bit length value"""
        return struct.pack('<I', length)