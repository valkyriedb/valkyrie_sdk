import struct

import pytest

from src.protocol.decoder import ProtocolDecoder
from src.protocol.types import DataType, CompositeType


class TestProtocolDecoder:
    def test_decode_bool_true(self):
        data = bytes([DataType.BOOL.value, 1])
        value, offset = ProtocolDecoder.decode_value(data)
        assert value is True
        assert offset == 2

    def test_decode_bool_false(self):
        data = bytes([DataType.BOOL.value, 0])
        value, offset = ProtocolDecoder.decode_value(data)
        assert value is False
        assert offset == 2

    def test_decode_int(self):
        test_int = -1234567890
        data = bytes([DataType.INT.value]) + struct.pack('<q', test_int)
        value, offset = ProtocolDecoder.decode_value(data)
        assert value == test_int
        assert offset == 9

    def test_decode_float(self):
        test_float = 3.141592653589793
        data = bytes([DataType.FLOAT.value]) + struct.pack('<d', test_float)
        value, offset = ProtocolDecoder.decode_value(data)
        assert value == test_float
        assert offset == 9

    def test_decode_string(self):
        test_str = "hello world"
        encoded_str = test_str.encode('utf-8')
        length_bytes = struct.pack('<I', len(encoded_str))
        data = bytes([DataType.STRING.value]) + length_bytes + encoded_str
        value, offset = ProtocolDecoder.decode_value(data)
        assert value == test_str
        assert offset == 1 + 4 + len(encoded_str)

    def test_decode_blob(self):
        test_blob = b'\x01\x02\x03\x04\x05'
        length_bytes = struct.pack('<I', len(test_blob))
        data = bytes([DataType.BLOB.value]) + length_bytes + test_blob
        value, offset = ProtocolDecoder.decode_value(data)
        assert value == test_blob
        assert offset == 1 + 4 + len(test_blob)

    def test_decode_array(self):
        int_val = 42
        str_val = "test"
        encoded_str = str_val.encode('utf-8')

        array_data = (
                bytes([CompositeType.ARRAY.value]) +
                struct.pack('<I', 2) +
                bytes([CompositeType.PRIMITIVE.value, DataType.INT.value]) +
                struct.pack('<q', int_val) +
                bytes([CompositeType.PRIMITIVE.value, DataType.STRING.value]) +
                struct.pack('<I', len(encoded_str)) +
                encoded_str
        )

        value, offset = ProtocolDecoder.decode_composite_value(array_data)
        assert isinstance(value, list)
        assert len(value) == 2
        assert value[0] == int_val
        assert value[1] == str_val

    def test_decode_map(self):
        key = "answer"
        encoded_key = key.encode('utf-8')
        val = 42

        map_data = (
                bytes([CompositeType.MAP.value]) +
                struct.pack('<I', 1) +
                bytes([CompositeType.PRIMITIVE.value, DataType.STRING.value]) +
                struct.pack('<I', len(encoded_key)) +
                encoded_key +
                bytes([CompositeType.PRIMITIVE.value, DataType.INT.value]) +
                struct.pack('<q', val)
        )

        value, offset = ProtocolDecoder.decode_composite_value(map_data)
        assert isinstance(value, dict)
        assert len(value) == 1
        assert value[key] == val

    def test_decode_length(self):
        test_length = 12345
        data = struct.pack('<I', test_length)
        length, offset = ProtocolDecoder.decode_length(data)
        assert length == test_length
        assert offset == 4

    def test_decode_string_direct(self):
        test_str = "direct string"
        encoded_str = test_str.encode('utf-8')
        data = struct.pack('<I', len(encoded_str)) + encoded_str
        value, offset = ProtocolDecoder.decode_string(data)
        assert value == test_str
        assert offset == 4 + len(encoded_str)

    def test_not_enough_data(self):
        with pytest.raises(ValueError, match="Not enough data to decode value"):
            ProtocolDecoder.decode_value(b'')

        with pytest.raises(ValueError, match="Not enough data for bool"):
            ProtocolDecoder.decode_value(bytes([DataType.BOOL.value]))

    def test_unknown_data_type(self):
        invalid_type = 99
        data = bytes([invalid_type])
        with pytest.raises(ValueError, match=f"Unknown data type: {invalid_type}"):
            ProtocolDecoder.decode_value(data)

    def test_unknown_composite_type(self):
        invalid_type = 99
        data = bytes([invalid_type])
        with pytest.raises(ValueError, match=f"Unknown composite type: {invalid_type}"):
            ProtocolDecoder.decode_composite_value(data)
