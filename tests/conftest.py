import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture
def mock_socket():
    from unittest.mock import Mock
    mock_sock = Mock()
    mock_sock.connect.return_value = None
    mock_sock.sendall.return_value = None
    mock_sock.recv.return_value = b''
    mock_sock.close.return_value = None
    return mock_sock

@pytest.fixture
def sample_response_packet():
    from src.protocol.packet import ResponsePacket
    from src.protocol.types import Status
    return ResponsePacket(Status.OK, "test_data")

