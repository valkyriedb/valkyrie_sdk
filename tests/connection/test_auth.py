import pytest
import struct
from unittest.mock import Mock
from src.connection.auth import AuthHandler
from src.connection.connection import TCPConnection
from src.protocol.types import Status
from src.exceptions.errors import ValkyrieAuthError


class TestAuthHandler:

    def test_init(self):
        mock_connection = Mock(spec=TCPConnection)
        auth = AuthHandler(mock_connection)
        assert auth.connection == mock_connection

    def test_authenticate_success(self):
        mock_connection = Mock(spec=TCPConnection)
        response_data = struct.pack('<I', 1) + bytes([Status.OK])
        mock_connection.receive.return_value = response_data

        auth = AuthHandler(mock_connection)
        auth.authenticate("password123")

        expected_password = "password123".encode('utf-8')
        expected_packet = struct.pack('<I', len(expected_password)) + expected_password
        mock_connection.send.assert_called_once_with(expected_packet)
        mock_connection.receive.assert_called_once_with(5)

    def test_authenticate_invalid_password(self):
        mock_connection = Mock(spec=TCPConnection)
        response_data = struct.pack('<I', 1) + bytes([Status.UNAUTHORIZED])
        mock_connection.receive.return_value = response_data

        auth = AuthHandler(mock_connection)

        with pytest.raises(ValkyrieAuthError, match="Authentication failed: Invalid password"):
            auth.authenticate("wrong_password")

        assert mock_connection.send.call_count == 3

    def test_authenticate_invalid_response_length(self):
        mock_connection = Mock(spec=TCPConnection)
        mock_connection.receive.return_value = b"123"  #

        auth = AuthHandler(mock_connection)

        with pytest.raises(ValkyrieAuthError, match="Invalid auth response"):
            auth.authenticate("password")

    def test_authenticate_unexpected_status(self):
        mock_connection = Mock(spec=TCPConnection)

        response_data = struct.pack('<I', 1) + bytes([Status.INTERNAL_ERROR])
        mock_connection.receive.return_value = response_data

        auth = AuthHandler(mock_connection)

        with pytest.raises(ValkyrieAuthError, match="Authentication failed: Unexpected status"):
            auth.authenticate("password")

    def test_authenticate_connection_error(self):
        mock_connection = Mock(spec=TCPConnection)
        mock_connection.send.side_effect = Exception("Network error")

        auth = AuthHandler(mock_connection)

        with pytest.raises(ValkyrieAuthError, match="Authentication error"):
            auth.authenticate("password")

    def test_authenticate_retry_logic(self):
        mock_connection = Mock(spec=TCPConnection)
        unauthorized_response = struct.pack('<I', 1) + bytes([Status.UNAUTHORIZED])
        success_response = struct.pack('<I', 1) + bytes([Status.OK])
        mock_connection.receive.side_effect = [
            unauthorized_response,
            unauthorized_response,
            success_response
        ]

        auth = AuthHandler(mock_connection)
        auth.authenticate("password")

        assert mock_connection.send.call_count == 3