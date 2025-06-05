import struct
from .connection import TCPConnection
from ..protocol.types import Status
from ..exceptions.errors import ValkyrieAuthError


class AuthHandler:
    def __init__(self, connection: TCPConnection):
        self.connection = connection

    def authenticate(self, password: str) -> None:
        max_attempts = 3

        for attempt in range(max_attempts):
            try:
                password_bytes = password.encode('utf-8')
                auth_packet = struct.pack('<I', len(password_bytes)) + password_bytes
                self.connection.send(auth_packet)
                response_data = self.connection.receive(5)

                if len(response_data) < 5:
                    raise ValkyrieAuthError("Invalid auth response")

                response_length = struct.unpack('<I', response_data[:4])[0]
                status = Status(response_data[4])


                if status == Status.OK:
                    return
                elif status == Status.UNAUTHORIZED:
                    if attempt == max_attempts - 1:
                        raise ValkyrieAuthError("Authentication failed: Invalid password")
                    continue
                else:
                    raise ValkyrieAuthError(f"Authentication failed: Unexpected status {status}")

            except ValkyrieAuthError:
                raise
            except Exception as e:
                raise ValkyrieAuthError(f"Authentication error: {e}")

        raise ValkyrieAuthError("Authentication failed after maximum attempts")