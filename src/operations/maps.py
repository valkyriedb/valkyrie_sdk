from typing import Any, List

from ..protocol.encoder import ProtocolEncoder
from ..protocol.packet import RequestPacket
from ..protocol.types import CompositeType, DataType, Operation


class MapOperations:
    def __init__(self, send_request_func):
        self._send_request = send_request_func

    def get(self, key: str, map_key: str) -> Any:
        map_key_bytes = ProtocolEncoder.encode_string(map_key)
        packet = RequestPacket(CompositeType.MAP, DataType.STRING, Operation.MAP_GET, key, map_key_bytes)
        response = self._send_request(packet)
        return response.data

    def set(self, key: str, map_key: str, value: Any) -> None:
        map_key_bytes = ProtocolEncoder.encode_string(map_key)
        value_bytes, data_type = ProtocolEncoder.encode_value(value)
        params = map_key_bytes + value_bytes
        packet = RequestPacket(CompositeType.MAP, data_type, Operation.MAP_SET, key, params)
        self._send_request(packet)

    def remove(self, key: str, map_key: str) -> None:
        map_key_bytes = ProtocolEncoder.encode_string(map_key)
        packet = RequestPacket(CompositeType.MAP, DataType.STRING, Operation.MAP_REMOVE, key, map_key_bytes)
        self._send_request(packet)

    def contains(self, key: str, map_key: str) -> bool:
        map_key_bytes = ProtocolEncoder.encode_string(map_key)
        packet = RequestPacket(CompositeType.MAP, DataType.STRING, Operation.MAP_CONTAINS, key, map_key_bytes)
        response = self._send_request(packet)
        return bool(response.data)


def keys(self, key: str) -> List[str]:
    packet = RequestPacket(CompositeType.MAP, DataType.STRING, Operation.MAP_KEYS, key)
    response = self._send_request(packet)
    return response.data if response.data else []


def values(self, key: str) -> List[Any]:
    packet = RequestPacket(CompositeType.MAP, DataType.STRING, Operation.MAP_VALUES, key)
    response = self._send_request(packet)
    return response.data if response.data else []
