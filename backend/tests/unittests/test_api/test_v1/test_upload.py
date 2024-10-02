from unittest.mock import MagicMock, patch

import use_cases
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@patch.object(use_cases, "upload_image", autospec=True)
class TestUpload:
    def test_returns_ok_when_upload_was_successful(self, mocked_upload_image: MagicMock) -> None:
        pass
