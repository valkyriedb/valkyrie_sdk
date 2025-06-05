import socket
import struct

from ..exceptions.errors import ValkyrieConnectionError


class TCPConnection:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False

    def connect(self) -> None:
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
        except Exception as e:
            if self.socket:
                self.socket.close()
                self.socket = None
            raise ValkyrieConnectionError(f"Failed to connect to {self.host}:{self.port}")

    def send(self, data: bytes) -> None:
        if not self.socket:
            raise ValkyrieConnectionError("Not connected")

        try:
            self.socket.sendall(data)
        except Exception as e:
            raise ValkyrieConnectionError(f"Failed to send data: {e}")

    def receive(self, length: int) -> bytes:
        if not self.socket:
            raise ValkyrieConnectionError("Not connected")

        data = b''
        while len(data) < length:
            try:
                chunk = self.socket.recv(length - len(data))
                if not chunk:
                    raise ValkyrieConnectionError("Connection closed by server")
                data += chunk
            except Exception as e:
                raise ValkyrieConnectionError(f"Failed to receive data: {e}")

        return data

    def receive_response(self) -> bytes:
        length_data = self.receive(4)

        response_length = struct.unpack('<I', length_data)[0]

        return self.receive(response_length)

    @property
    def is_connected(self) -> bool:
        return self.socket is not None

    def disconnect(self) -> None:
        if self.socket:
            self.socket.close()
            self.socket = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
