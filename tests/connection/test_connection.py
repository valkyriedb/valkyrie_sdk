import pytest
import socket
from unittest.mock import Mock, patch, MagicMock
from src.connection.connection import TCPConnection
from src.exceptions.errors import ValkyrieConnectionError
import struct

class TestTCPConnection:

    def test_init(self):
        conn = TCPConnection("localhost", 8080)
        assert conn.host == "localhost"
        assert conn.port == 8080
        assert conn.socket is None
        assert conn.connected is False

    @patch('socket.socket')
    def test_connect_success(self, mock_socket_class):
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket

        conn = TCPConnection("localhost", 8080)
        conn.connect()

        mock_socket_class.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_socket.connect.assert_called_once_with(("localhost", 8080))
        assert conn.socket == mock_socket

    @patch('socket.socket')
    def test_connect_failure(self, mock_socket_class):
        mock_socket = Mock()
        mock_socket.connect.side_effect = Exception("Connection failed")
        mock_socket_class.return_value = mock_socket

        conn = TCPConnection("localhost", 8080)

        with pytest.raises(ValkyrieConnectionError, match="Failed to connect"):
            conn.connect()

        mock_socket.close.assert_called_once()
        assert conn.socket is None

    def test_send_not_connected(self):
        conn = TCPConnection("localhost", 8080)

        with pytest.raises(ValkyrieConnectionError, match="Not connected"):
            conn.send(b"test")

    def test_send_success(self):
        conn = TCPConnection("localhost", 8080)
        mock_socket = Mock()
        conn.socket = mock_socket

        test_data = b"test_data"
        conn.send(test_data)

        mock_socket.sendall.assert_called_once_with(test_data)

    def test_send_failure(self):
        conn = TCPConnection("localhost", 8080)
        mock_socket = Mock()
        mock_socket.sendall.side_effect = Exception("Send failed")
        conn.socket = mock_socket

        with pytest.raises(ValkyrieConnectionError, match="Failed to send data"):
            conn.send(b"test")

    def test_receive_not_connected(self):
        conn = TCPConnection("localhost", 8080)

        with pytest.raises(ValkyrieConnectionError, match="Not connected"):
            conn.receive(4)

    def test_receive_success(self):
        conn = TCPConnection("localhost", 8080)
        mock_socket = Mock()
        mock_socket.recv.return_value = b"test"
        conn.socket = mock_socket

        result = conn.receive(4)

        assert result == b"test"
        mock_socket.recv.assert_called_once_with(4)

    def test_receive_partial_data(self):
        conn = TCPConnection("localhost", 8080)
        mock_socket = Mock()
        mock_socket.recv.side_effect = [b"te", b"st"]
        conn.socket = mock_socket

        result = conn.receive(4)
        assert result == b"test"
        assert mock_socket.recv.call_count == 2

    def test_receive_connection_closed(self):
        conn = TCPConnection("localhost", 8080)
        mock_socket = Mock()
        mock_socket.recv.return_value = b""
        conn.socket = mock_socket

        with pytest.raises(ValkyrieConnectionError, match="Connection closed by server"):
            conn.receive(4)

    def test_receive_response(self):
        conn = TCPConnection("localhost", 8080)
        mock_socket = Mock()
        response_data = b"test_response"
        length_bytes = struct.pack('<I', len(response_data))
        mock_socket.recv.side_effect = [length_bytes, response_data]
        conn.socket = mock_socket

        result = conn.receive_response()
        assert result == response_data

    def test_is_connected_property(self):
        conn = TCPConnection("localhost", 8080)
        assert not conn.is_connected

        conn.socket = Mock()
        assert conn.is_connected

    def test_disconnect(self):
        conn = TCPConnection("localhost", 8080)
        mock_socket = Mock()
        conn.socket = mock_socket

        conn.disconnect()

        mock_socket.close.assert_called_once()
        assert conn.socket is None

    def test_context_manager(self):
        with patch('socket.socket') as mock_socket_class:
            mock_socket = Mock()
            mock_socket_class.return_value = mock_socket

            with TCPConnection("localhost", 8080) as conn:
                assert conn.socket == mock_socket

            mock_socket.close.assert_called_once()