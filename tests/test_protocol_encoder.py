import pytest
import struct
from src.protocol.encoder import ProtocolEncoder
from src.protocol.types import DataType, CompositeType


class TestProtocolEncoder:

    def test_encode_type_byte(self):
        result = ProtocolEncoder.encode_type_byte(CompositeType.PRIMITIVE, DataType.STRING)
        expected = (CompositeType.PRIMITIVE << 4) | DataType.STRING
        assert result == expected

    def test_encode_bool_true(self):
        result = ProtocolEncoder.encode_value(True)
        expected = bytes([DataType.BOOL]) + bytes([1])
        assert result == expected

    def test_encode_bool_false(self):
        result = ProtocolEncoder.encode_value(False)
        expected = bytes([DataType.BOOL]) + bytes([0])
        assert result == expected

    def test_encode_int(self):
        result = ProtocolEncoder.encode_value(42)
        expected = bytes([DataType.INT]) + struct.pack('<q', 42)
        assert result == expected

    def test_encode_float(self):
        result = ProtocolEncoder.encode_value(3.14)
        expected = bytes([DataType.FLOAT]) + struct.pack('<d', 3.14)
        assert result == expected

    def test_encode_string(self):
        test_string = "hello"
        result = ProtocolEncoder.encode_value(test_string)
        expected = (bytes([DataType.STRING]) +
                   struct.pack('<I', len(test_string.encode('utf-8'))) +
                   test_string.encode('utf-8'))
        assert result == expected

    def test_encode_bytes(self):
        test_bytes = b"binary data"
        result = ProtocolEncoder.encode_value(test_bytes)
        expected = bytes([DataType.BLOB]) + struct.pack('<I', len(test_bytes)) + test_bytes
        assert result == expected

    def test_encode_bytearray(self):
        test_bytearray = bytearray(b"test data")
        result = ProtocolEncoder.encode_value(test_bytearray)
        expected = bytes([DataType.BLOB]) + struct.pack('<I', len(test_bytearray)) + test_bytearray
        assert result == expected

    def test_encode_unsupported_type(self):
        with pytest.raises(ValueError, match="Unsupported value type"):
            ProtocolEncoder.encode_value([1, 2, 3])

    def test_encode_string_method(self):
        test_string = "test"
        result = ProtocolEncoder.encode_string(test_string)
        expected = struct.pack('<I', len(test_string.encode('utf-8'))) + test_string.encode('utf-8')
        assert result == expected

    def test_encode_length(self):
        length = 1024
        result = ProtocolEncoder.encode_length(length)
        expected = struct.pack('<I', length)
        assert result == expected

    def test_encode_empty_string(self):
        result = ProtocolEncoder.encode_value("")
        expected = bytes([DataType.STRING]) + struct.pack('<I', 0)
        assert result == expected

    def test_encode_unicode_string(self):
        test_string = "hello world"
        result = ProtocolEncoder.encode_value(test_string)
        encoded_bytes = test_string.encode('utf-8')
        expected = (bytes([DataType.STRING]) +
                   struct.pack('<I', len(encoded_bytes)) +
                   encoded_bytes)
        assert result == expected