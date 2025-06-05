import struct
from typing import Any, Tuple


class ProtocolDecoder:
    @staticmethod
    def decode_value(data: bytes, offset: int = 0) -> Tuple[Any, int]:
        if offset >= len(data):
            raise ValueError("Not enough data to decode value")

        if offset + 4 <= len(data):
            try:
                length = struct.unpack('<I', data[offset:offset + 4])[0]
                if offset + 4 + length <= len(data):
                    value_data = data[offset + 4:offset + 4 + length]
                    try:
                        return value_data.decode('utf-8'), offset + 4 + length
                    except UnicodeDecodeError:
                        return value_data, offset + 4 + length
            except struct.error:
                pass

        if offset + 8 <= len(data):
            try:
                value = struct.unpack('<q', data[offset:offset + 8])[0]
                float_val = struct.unpack('<d', data[offset:offset + 8])[0]
                if abs(float_val - value) < 1e-10:
                    return value, offset + 8
                else:
                    return float_val, offset + 8
            except struct.error:
                pass

        if offset + 1 <= len(data):
            value = data[offset]
            if value in (0, 1):
                return bool(value), offset + 1

        raise ValueError("Unable to decode value from data")

    @staticmethod
    def decode_length(data: bytes, offset: int = 0) -> Tuple[int, int]:
        if offset + 4 > len(data):
            raise ValueError("Not enough data for length")
        length = struct.unpack('<I', data[offset:offset + 4])[0]
        return length, offset + 4

    @staticmethod
    def decode_string(data: bytes, offset: int = 0) -> Tuple[str, int]:
        length, new_offset = ProtocolDecoder.decode_length(data, offset)
        if new_offset + length > len(data):
            raise ValueError("Not enough data for string")
        string_data = data[new_offset:new_offset + length]
        return string_data.decode('utf-8'), new_offset + length
