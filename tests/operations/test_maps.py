import pytest
from unittest.mock import Mock
from src.operations.maps import MapOperations
from src.protocol.packet import RequestPacket, ResponsePacket
from src.protocol.types import CompositeType, DataType, Operation, Status


class TestMapOperations:

    @pytest.fixture
    def mock_send_request(self):
        return Mock()

    @pytest.fixture
    def maps(self, mock_send_request):
        return MapOperations(mock_send_request)

    def test_get(self, maps, mock_send_request):
        mock_response = ResponsePacket(Status.OK, "map_value")
        mock_send_request.return_value = mock_response

        result = maps.get("map_key", "field_key")

        assert result == "map_value"
        mock_send_request.assert_called_once()

        call_args = mock_send_request.call_args[0][0]
        assert call_args.composite == CompositeType.MAP
        assert call_args.operation == Operation.MAP_GET
        assert call_args.key == "map_key"
        assert len(call_args.params) > 0

    def test_set(self, maps, mock_send_request):
        mock_response = ResponsePacket(Status.OK)
        mock_send_request.return_value = mock_response

        maps.set("map_key", "field_key", "field_value")

        mock_send_request.assert_called_once()
        call_args = mock_send_request.call_args[0][0]
        assert call_args.composite == CompositeType.MAP
        assert call_args.operation == Operation.MAP_SET
        assert call_args.key == "map_key"
        assert len(call_args.params) > 0

    def test_remove(self, maps, mock_send_request):
        mock_response = ResponsePacket(Status.OK)
        mock_send_request.return_value = mock_response

        maps.remove("map_key", "field_key")

        mock_send_request.assert_called_once()
        call_args = mock_send_request.call_args[0][0]
        assert call_args.operation == Operation.MAP_REMOVE
        assert call_args.key == "map_key"

    def test_contains(self, maps, mock_send_request):
        mock_response = ResponsePacket(Status.OK, True)
        mock_send_request.return_value = mock_response

        result = maps.contains("map_key", "field_key")

        assert result is True
        mock_send_request.assert_called_once()
        call_args = mock_send_request.call_args[0][0]
        assert call_args.operation == Operation.MAP_CONTAINS