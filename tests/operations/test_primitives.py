import pytest
from unittest.mock import Mock
from src.operations.primitives import PrimitiveOperations
from src.protocol.packet import RequestPacket, ResponsePacket
from src.protocol.types import CompositeType, DataType, Operation, Status
from unittest.mock import patch

class TestPrimitiveOperations:
    """Test suite for PrimitiveOperations"""

    @pytest.fixture
    def mock_send_request(self):
        return Mock()

    @pytest.fixture
    def primitives(self, mock_send_request):
        return PrimitiveOperations(mock_send_request)

    def test_get(self, primitives, mock_send_request):
        mock_response = ResponsePacket(Status.OK, "test_value")
        mock_send_request.return_value = mock_response

        result = primitives.get("test_key")

        assert result == "test_value"
        mock_send_request.assert_called_once()

        # Verify the request packet
        call_args = mock_send_request.call_args[0][0]
        assert isinstance(call_args, RequestPacket)
        assert call_args.composite == CompositeType.PRIMITIVE
        assert call_args.primitive == DataType.STRING
        assert call_args.operation == Operation.GET
        assert call_args.key == "test_key"

    def test_set(self, primitives, mock_send_request):
        mock_response = ResponsePacket(Status.OK)
        mock_send_request.return_value = mock_response

        with patch('src.operations.primitives.ProtocolEncoder.encode_value') as mock_encode:
            mock_encode.return_value = (b'encoded_value', DataType.STRING)
            primitives.set("test_key", "test_value")

        mock_send_request.assert_called_once()
        call_args = mock_send_request.call_args[0][0]
        assert call_args.composite == CompositeType.PRIMITIVE
        assert call_args.primitive == DataType.STRING
        assert call_args.operation == Operation.SET
        assert call_args.key == "test_key"
        assert call_args.params == b'encoded_value'

    def test_remove(self, primitives, mock_send_request):
        mock_response = ResponsePacket(Status.OK)
        mock_send_request.return_value = mock_response

        primitives.remove("test_key")

        mock_send_request.assert_called_once()
        call_args = mock_send_request.call_args[0][0]
        assert call_args.operation == Operation.REMOVE
        assert call_args.key == "test_key"

    def test_length(self, primitives, mock_send_request):
        mock_response = ResponsePacket(Status.OK, 42)
        mock_send_request.return_value = mock_response

        result = primitives.length("test_key")

        assert result == 42
        mock_send_request.assert_called_once()
        call_args = mock_send_request.call_args[0][0]
        assert call_args.operation == Operation.LEN
        assert call_args.key == "test_key"

    def test_append(self, primitives, mock_send_request):
        mock_response = ResponsePacket(Status.OK)
        mock_send_request.return_value = mock_response

        primitives.append("test_key", "suffix")

        mock_send_request.assert_called_once()
        call_args = mock_send_request.call_args[0][0]
        assert call_args.operation == Operation.APPEND
        assert call_args.key == "test_key"
        assert len(call_args.params) > 0

    def test_increment(self, primitives, mock_send_request):
        mock_response = ResponsePacket(Status.OK, 43)
        mock_send_request.return_value = mock_response

        result = primitives.increment("counter")

        assert result == 43
        mock_send_request.assert_called_once()
        call_args = mock_send_request.call_args[0][0]
        assert call_args.operation == Operation.INCREMENT
        assert call_args.primitive == DataType.INT
        assert call_args.key == "counter"

    def test_decrement(self, primitives, mock_send_request):
        mock_response = ResponsePacket(Status.OK, 41)
        mock_send_request.return_value = mock_response

        result = primitives.decrement("counter")

        assert result == 41
        mock_send_request.assert_called_once()
        call_args = mock_send_request.call_args[0][0]
        assert call_args.operation == Operation.DECREMENT
        assert call_args.primitive == DataType.INT
        assert call_args.key == "counter"