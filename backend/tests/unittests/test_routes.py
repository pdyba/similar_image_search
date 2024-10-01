from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from backend.src.main import app


client = TestClient(app)


def test_health(monkeypatch: MagicMock):

    response = client.get("/v1/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}
