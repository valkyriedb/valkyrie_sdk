import struct
from typing import Any
from .types import CompositeType, DataType, Operation, Status
from .encoder import ProtocolEncoder
from .decoder import ProtocolDecoder


class RequestPacket:
    def __init__(self, composite: CompositeType, primitive: DataType,
                 operation: Operation, key: str, params: bytes = b''):
        self.composite = composite
        self.primitive = primitive
        self.operation = operation
        self.key = key
        self.params = params

    def to_bytes(self) -> bytes:
        key_bytes = self.key.encode('utf-8')

        type_byte = ProtocolEncoder.encode_type_byte(self.composite, self.primitive)
        packet_data = struct.pack('<BB', type_byte, self.operation)
        packet_data += struct.pack('<I', len(key_bytes)) + key_bytes
        packet_data += self.params

        return struct.pack('<I', len(packet_data)) + packet_data


class ResponsePacket:
    def __init__(self, status: Status, data: Any = None):
        self.status = status
        self.data = data

    @classmethod
    def from_bytes(cls, data: bytes) -> 'ResponsePacket':
        if len(data) < 1:
            raise ValueError("Response too short")

        status = Status(data[0])
        response_data = None

        if len(data) > 1:
            try:
                response_data, _ = ProtocolDecoder.decode_value(data[1:])
            except:
                remaining_data = data[1:]
                if len(remaining_data) >= 4:
                    data_length = struct.unpack('<I', remaining_data[:4])[0]
                    if len(remaining_data) >= 4 + data_length:
                        raw_data = remaining_data[4:4 + data_length]
                        try:
                            response_data = raw_data.decode('utf-8')
                        except UnicodeDecodeError:
                            response_data = raw_data
                    else:
                        response_data = remaining_data
                else:
                    response_data = remaining_data

        return cls(status, response_data)