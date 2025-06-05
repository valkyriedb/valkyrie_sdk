import struct
from typing import Any, Tuple

from .types import DataType, CompositeType


class ProtocolDecoder:
    @staticmethod
    def decode_value(data: bytes, offset: int = 0) -> Tuple[Any, int]:
        if offset >= len(data):
            raise ValueError("Not enough data to decode value")

        type_byte = data[offset]
        offset += 1

        try:
            data_type = DataType(type_byte)
        except ValueError:
            raise ValueError(f"Unknown data type: {type_byte}")

        if data_type == DataType.BOOL:
            if offset + 1 > len(data):
                raise ValueError("Not enough data for bool")
            bool_val = bool(data[offset])
            return bool_val, offset + 1

        elif data_type == DataType.INT:
            if offset + 8 > len(data):
                raise ValueError("Not enough data for int")
            int_val = struct.unpack('<q', data[offset:offset + 8])[0]
            return int_val, offset + 8

        elif data_type == DataType.FLOAT:
            if offset + 8 > len(data):
                raise ValueError("Not enough data for float")
            float_val = struct.unpack('<d', data[offset:offset + 8])[0]
            return float_val, offset + 8

        elif data_type == DataType.STRING:
            length, new_offset = ProtocolDecoder.decode_length(data, offset)
            if new_offset + length > len(data):
                raise ValueError("Not enough data for string")
            string_data = data[new_offset:new_offset + length]
            return string_data.decode('utf-8'), new_offset + length

        elif data_type == DataType.BLOB:
            length, new_offset = ProtocolDecoder.decode_length(data, offset)
            if new_offset + length > len(data):
                raise ValueError("Not enough data for blob")
            blob_data = data[new_offset:new_offset + length]
            return blob_data, new_offset + length

        else:
            raise ValueError(f"Unsupported data type: {data_type}")


    @staticmethod
    def decode_composite_value(data: bytes, offset: int = 0) -> Tuple[Any, int]:
        if offset >= len(data):
            raise ValueError("Not enough data to decode composite value")

        composite_type_byte = data[offset]
        offset += 1

        try:
            composite_type = CompositeType(composite_type_byte)
        except ValueError:
            raise ValueError(f"Unknown composite type: {composite_type_byte}")

        if composite_type == CompositeType.PRIMITIVE:
            return ProtocolDecoder.decode_value(data, offset)

        elif composite_type == CompositeType.ARRAY:
            return ProtocolDecoder.decode_array(data, offset)

        elif composite_type == CompositeType.MAP:
            return ProtocolDecoder.decode_map(data, offset)

        else:
            raise ValueError(f"Unsupported composite type: {composite_type}")

    @staticmethod
    def decode_array(data: bytes, offset: int = 0) -> Tuple[list, int]:
        """Decode an array of values."""
        length, offset = ProtocolDecoder.decode_length(data, offset)
        array = []

        for _ in range(length):
            value, offset = ProtocolDecoder.decode_composite_value(data, offset)
            array.append(value)

        return array, offset

    @staticmethod
    def decode_map(data: bytes, offset: int = 0) -> Tuple[dict, int]:
        """Decode a map (dictionary) of key-value pairs."""
        length, offset = ProtocolDecoder.decode_length(data, offset)
        map_dict = {}

        for _ in range(length):
            key, offset = ProtocolDecoder.decode_composite_value(data, offset)
            value, offset = ProtocolDecoder.decode_composite_value(data, offset)
            map_dict[key] = value

        return map_dict, offset

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
