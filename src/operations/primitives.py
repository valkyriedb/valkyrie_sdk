from typing import Any
from src.protocol.types import CompositeType, DataType, Operation
from src.protocol.encoder import ProtocolEncoder
from src.protocol.packet import RequestPacket


class PrimitiveOperations:
    def __init__(self, send_request_func):
        self._send_request = send_request_func

    def get(self, key: str) -> Any:
        packet = RequestPacket(CompositeType.PRIMITIVE, DataType.STRING, Operation.GET, key)
        response = self._send_request(packet)
        return response.data

    def set(self, key: str, value: Any) -> None:
        value_bytes, data_type = ProtocolEncoder.encode_value(value)
        packet = RequestPacket(CompositeType.PRIMITIVE, data_type, Operation.SET, key, value_bytes)
        self._send_request(packet)

    def remove(self, key: str) -> None:
        packet = RequestPacket(CompositeType.PRIMITIVE, DataType.STRING, Operation.REMOVE, key)
        self._send_request(packet)

    def length(self, key: str) -> int:
        packet = RequestPacket(CompositeType.PRIMITIVE, DataType.STRING, Operation.LEN, key)
        response = self._send_request(packet)
        return response.data

    def append(self, key: str, value: str) -> None:
        value_bytes = ProtocolEncoder.encode_string(value)
        packet = RequestPacket(CompositeType.PRIMITIVE, DataType.STRING, Operation.APPEND, key, value_bytes)
        self._send_request(packet)

    def increment(self, key: str) -> int:
        packet = RequestPacket(CompositeType.PRIMITIVE, DataType.INT, Operation.INCREMENT, key)
        response = self._send_request(packet)
        return response.data

    def decrement(self, key: str) -> int:
        packet = RequestPacket(CompositeType.PRIMITIVE, DataType.INT, Operation.DECREMENT, key)
        response = self._send_request(packet)
        return response.data
