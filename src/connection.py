import socket


class TCPConnection:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self):
        try:
            self.sock.connect((self.host, self.port))
            self.sock.settimeout(1)
            self.connected = True
        except socket.error as e:
            raise ConnectionError(f"Failed to connect: {e}")

    def set_timeout(self, timeout):
        self.sock.settimeout(timeout)

    def send(self, data):
        if not self.connected:
            raise ConnectionError("Not connected to the server")
        try:
            self.sock.sendall(data)
        except socket.error as e:
            self.connected = False
            raise ConnectionError(f"Send failed: {e}")

    def recv(self, buffer_size=1024):
        if not self.connected:
            raise ConnectionError("Not connected to the server")
        data = self.sock.recv(buffer_size)
        if not data:
            self.connected = False
            raise ConnectionError(f"Connection closed: received empty response from the server.")

    def close(self):
        self.sock.close()
        self.connected = False

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
