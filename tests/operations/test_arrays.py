import pytest
from unittest.mock import Mock
from src.operations.arrays import ArrayOperations
from src.protocol.packet import RequestPacket, ResponsePacket
from src.protocol.types import CompositeType, DataType, Operation, Status


class TestArrayOperations:

    @pytest.fixture
    def mock_send_request(self):
        return Mock()

    @pytest.fixture
    def arrays(self, mock_send_request):
        return ArrayOperations(mock_send_request)

    def test_slice(self, arrays, mock_send_request):
        mock_response = ResponsePacket(Status.OK, ["item1", "item2", "item3"])
        mock_send_request.return_value = mock_response

        result = arrays.slice("array_key", 0, 3)

        assert result == ["item1", "item2", "item3"]
        mock_send_request.assert_called_once()

        call_args = mock_send_request.call_args[0][0]
        assert call_args.composite == CompositeType.ARRAY
        assert call_args.operation == Operation.SLICE
        assert call_args.key == "array_key"

    def test_slice_empty_response(self, arrays, mock_send_request):
        mock_response = ResponsePacket(Status.OK, None)
        mock_send_request.return_value = mock_response

        result = arrays.slice("array_key", 0, 0)

        assert result == []

    def test_insert(self, arrays, mock_send_request):
        mock_response = ResponsePacket(Status.OK)
        mock_send_request.return_value = mock_response

        arrays.insert("array_key", 1, ["new_item1", "new_item2"])

        mock_send_request.assert_called_once()
        call_args = mock_send_request.call_args[0][0]
        assert call_args.operation == Operation.INSERT
        assert call_args.key == "array_key"
        assert len(call_args.params) > 4

    def test_remove(self, arrays, mock_send_request):
        mock_response = ResponsePacket(Status.OK)
        mock_send_request.return_value = mock_response