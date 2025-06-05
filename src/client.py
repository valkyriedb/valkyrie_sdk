from typing import Optional
from src.connection.connection import TCPConnection
from src.connection.auth import AuthHandler
from src.protocol.packet import RequestPacket, ResponsePacket
from src.protocol.types import Status
from src.operations.primitives import PrimitiveOperations
from src.operations.maps import MapOperations
from src.operations.arrays import ArrayOperations
from src.exceptions.errors import (
    ValkyrieError, ValkyrieConnectionError, ValkyrieRequestError,
    ValkyrieServerError, ValkyrieAuthError
)


class ValkyrieClient:

    def __init__(self, host: str = 'localhost', port: int = 8080, password: str = ''):
        self.host = host
        self.port = port
        self.password = password

        self.connection: Optional[TCPConnection] = None
        self.auth_handler: Optional[AuthHandler] = None

        self.primitives: Optional[PrimitiveOperations] = None
        self.maps: Optional[MapOperations] = None
        self.arrays: Optional[ArrayOperations] = None


    def connect(self) -> None:
        try:
            self.connection = TCPConnection(self.host, self.port)
            self.connection.connect()

            self.auth_handler = AuthHandler(self.connection)
            self.auth_handler.authenticate(self.password)

            self.primitives = PrimitiveOperations(self._send_request)
            self.maps = MapOperations(self._send_request)
            self.arrays = ArrayOperations(self._send_request)


        except Exception as e:
            self.disconnect()
            raise ValkyrieConnectionError(f"Failed to connect: {e}")

    def disconnect(self) -> None:
        if self.connection:
            self.connection.disconnect()
            self.connection = None
            self.auth_handler = None
            self.primitives = None
            self.maps = None
            self.arrays = None

    def _send_request(self, packet: RequestPacket) -> ResponsePacket:
        if not self.connection or not self.connection.is_connected:
            raise ValkyrieConnectionError("Not connected to server")

        try:
            request_bytes = packet.to_bytes()
            self.connection.send(request_bytes)

            response_bytes = self.connection.receive_response()
            response = ResponsePacket.from_bytes(response_bytes)

            if response.status != Status.OK:
                self._handle_error_status(response.status)

            return response

        except ValkyrieError:
            raise
        except Exception as e:
            raise ValkyrieConnectionError(f"Communication error: {e}")

    @staticmethod
    def _handle_error_status(status: Status) -> None:
        error_messages = {
            Status.INVALID_REQUEST: "Invalid request",
            Status.UNAVAILABLE_OPERATION: "Unavailable operation",
            Status.UNAUTHORIZED: "Unauthorized access",
            Status.NOT_FOUND: "Key not found",
            Status.WRONG_TYPE: "Wrong data type",
            Status.OUT_OF_RANGE: "Index out of range",
            Status.INTERNAL_ERROR: "Internal server error"
        }

        message = error_messages.get(status, f"Unknown error (status: {status})")

        if status in (Status.INVALID_REQUEST, Status.UNAVAILABLE_OPERATION):
            raise ValkyrieRequestError(message)
        elif status == Status.UNAUTHORIZED:
            raise ValkyrieAuthError(message)
        else:
            raise ValkyrieServerError(message)

    @property
    def is_connected(self) -> bool:
        return (self.connection is not None and
                self.connection.is_connected and
                self.primitives is not None)

    def get(self, key: str):
        if not self.primitives:
            raise ValkyrieConnectionError("Not connected")
        return self.primitives.get(key)

    def set(self, key: str, value):
        if not self.primitives:
            raise ValkyrieConnectionError("Not connected")
        return self.primitives.set(key, value)

    def remove(self, key: str):
        if not self.primitives:
            raise ValkyrieConnectionError("Not connected")
        return self.primitives.remove(key)

    def length(self, key: str):
        if not self.primitives:
            raise ValkyrieConnectionError("Not connected")
        return self.primitives.length(key)

    def append(self, key: str, value: str):
        if not self.primitives:
            raise ValkyrieConnectionError("Not connected")
        return self.primitives.append(key, value)

    def increment(self, key: str):
        if not self.primitives:
            raise ValkyrieConnectionError("Not connected")
        return self.primitives.increment(key)

    def decrement(self, key: str):
        if not self.primitives:
            raise ValkyrieConnectionError("Not connected")
        return self.primitives.decrement(key)


    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


#