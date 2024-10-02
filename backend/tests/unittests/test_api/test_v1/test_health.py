from unittest.mock import MagicMock, patch

from db import MilvusConnector
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@patch.object(MilvusConnector, "get_collection_stats", autospec=True)
class TestHealth:
    def test_returns_ok_when_db_is_accessable(
        self, mocked_get_collection_stats: MagicMock
    ) -> None:
        mocked_get_collection_stats.return_value = {"row_count": 10}

        response = client.get("/v1/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
        mocked_get_collection_stats.assert_called_once()

    def test_returns_error_status_when_db_is_not_accessable(
        self, mocked_get_collection_stats: MagicMock
    ) -> None:
        mocked_get_collection_stats.return_value = None

        response = client.get("/v1/health")

        assert response.status_code == 500
        assert response.json() == {"status": "error"}
        mocked_get_collection_stats.assert_called_once()
