from unittest.mock import MagicMock, patch

import use_cases
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@patch.object(use_cases, "get_image_by_id", autospec=True)
class TestDownload:
    def test_returns_image_link_file_found(self, mocked_get_image_by_id: MagicMock) -> None:
        pass
