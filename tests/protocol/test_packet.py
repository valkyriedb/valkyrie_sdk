import pytest
import struct
from src.protocol.packet import RequestPacket, ResponsePacket
from src.protocol.types import CompositeType, DataType, Operation, Status


class TestRequestPacket:

    def test_create_request_packet(self):
        packet = RequestPacket(
            CompositeType.PRIMITIVE,
            DataType.STRING,
            Operation.GET,
            "test_key"
        )
        assert packet.composite == CompositeType.PRIMITIVE
        assert packet.primitive == DataType.STRING
        assert packet.operation == Operation.GET
        assert packet.key == "test_key"
        assert packet.params == b''

    def test_create_request_packet_with_params(self):
        params = b"test_params"
        packet = RequestPacket(
            CompositeType.PRIMITIVE,
            DataType.STRING,
            Operation.SET,
            "test_key",
            params
        )
        assert packet.params == params

    def test_request_packet_to_bytes(self):
        packet = RequestPacket(
            CompositeType.PRIMITIVE,
            DataType.STRING,
            Operation.GET,
            "key"
        )
        result = packet.to_bytes()

        assert isinstance(result, bytes)
        assert len(result) > 4
        packet_length = struct.unpack('<I', result[:4])[0]
        assert packet_length == len(result) - 4

    def test_request_packet_to_bytes_with_params(self):
        params = struct.pack('<I', 42)
        packet = RequestPacket(
            CompositeType.PRIMITIVE,
            DataType.INT,
            Operation.SET,
            "counter",
            params
        )
        result = packet.to_bytes()
        assert isinstance(result, bytes)
        assert len(result) > len(params) + 4


class TestResponsePacket:

    def test_create_response_packet(self):
        packet = ResponsePacket(Status.OK, "test_data")
        assert packet.status == Status.OK
        assert packet.data == "test_data"

    def test_create_response_packet_no_data(self):
        packet = ResponsePacket(Status.OK)
        assert packet.status == Status.OK
        assert packet.data is None

    def test_response_packet_from_bytes_with_data(self):
        test_data = "hello"
        encoded_data = struct.pack('<I', len(test_data)) + test_data.encode('utf-8')
        response_bytes = bytes([Status.OK]) + encoded_data

        packet = ResponsePacket.from_bytes(response_bytes)
        assert packet.status == Status.OK
        assert packet.data == test_data

    def test_response_packet_from_bytes_status_only(self):
        response_bytes = bytes([Status.NOT_FOUND])
        packet = ResponsePacket.from_bytes(response_bytes)
        assert packet.status == Status.NOT_FOUND
        assert packet.data is None

    def test_response_packet_from_bytes_empty_raises_error(self):
        with pytest.raises(ValueError, match="Response too short"):
            ResponsePacket.from_bytes(b'')

    def test_response_packet_from_bytes_invalid_data(self):
        response_bytes = bytes([Status.OK, 0xFF, 0xFE])
        packet = ResponsePacket.from_bytes(response_bytes)
        assert packet.status == Status.OK
        assert packet.data == bytes([0xFF, 0xFE])