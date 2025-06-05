import struct
from typing import Any, List
from ..protocol.types import CompositeType, DataType, Operation
from ..protocol.encoder import ProtocolEncoder
from ..protocol.packet import RequestPacket


class ArrayOperations:
    def __init__(self, send_request_func):
        self._send_request = send_request_func

    def slice(self, key: str, start: int, end: int) -> List[Any]:
        params = struct.pack('<II', start, end)
        packet = RequestPacket(CompositeType.ARRAY, DataType.STRING, Operation.SLICE, key, params)
        response = self._send_request(packet)
        return response.data if response.data else []

    def insert(self, key: str, index: int, values: List[Any]) -> None:
        params = struct.pack('<I', index)

        if values:
            first_value_data_type = ProtocolEncoder.get_data_type(values[0])
        else:
            first_value_data_type = DataType.STRING  # Default fallback

        for value in values:
            value_bytes = ProtocolEncoder.encode_value(value)  # Only one return value
            params += value_bytes

        packet = RequestPacket(CompositeType.ARRAY, first_value_data_type, Operation.INSERT, key, params)
        self._send_request(packet)

    def remove(self, key: str, start: int, end: int) -> None:
        params = struct.pack('<II', start, end)
        packet = RequestPacket(CompositeType.ARRAY, DataType.STRING, Operation.ARRAY_REMOVE, key, params)
        self._send_request(packet)

    def length(self, key: str) -> int:
        packet = RequestPacket(CompositeType.ARRAY, DataType.STRING, Operation.LEN, key)
        response = self._send_request(packet)
        return response.data