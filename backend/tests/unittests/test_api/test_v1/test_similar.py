from unittest.mock import MagicMock, patch

import use_cases
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@patch.object(use_cases, "find_similar_images_using_id", autospec=True)
class TestSimilar:
    def test_returns_similar_images_when_found_using_default_params(
        self, mocked_find_similar_images_using_id: MagicMock
    ) -> None:
        img_id = "123123"
        mocked_find_similar_images_using_id.return_value = [
            {
                "id": "321321",
                "url": "http://s3-link/file.png",
                "similarity_score": 98.991231,
            }
        ]

        response = client.get(f"/v1/similar/{img_id}")

        assert response.status_code == 200
        assert response.json() == {
            "id": img_id,
            "similar_images": [
                {
                    "id": "321321",
                    "url": "http://s3-link/file.png",
                    "similarity_score": 98.991231,
                }
            ],
        }
        mocked_find_similar_images_using_id.assert_called_once_with(
            img_id, limit=10, precision=0.99
        )

    def test_returns_similar_images_when_found_using_custom_params(
        self, mocked_find_similar_images_using_id: MagicMock
    ) -> None:
        img_id = "123123"
        mocked_find_similar_images_using_id.return_value = [
            {
                "id": "321321",
                "url": "http://s3-link/file.png",
                "similarity_score": 98.991231,
            }
        ]

        response = client.get(f"/v1/similar/{img_id}?limit=2&precision=0.5")

        assert response.status_code == 200
        assert response.json() == {
            "id": img_id,
            "similar_images": [
                {
                    "id": "321321",
                    "url": "http://s3-link/file.png",
                    "similarity_score": 98.991231,
                }
            ],
        }
        mocked_find_similar_images_using_id.assert_called_once_with(img_id, limit=2, precision=0.5)

    def test_return_404_when_requested_image_does_not_exists(
        self, mocked_find_similar_images_using_id: MagicMock
    ) -> None:
        img_id = "123123"
        mocked_find_similar_images_using_id.return_value = None

        response = client.get(f"/v1/similar/{img_id}")

        assert response.status_code == 404
        assert response.json() == {"detail": "Image not found"}
        mocked_find_similar_images_using_id.assert_called_once_with(
            img_id, limit=10, precision=0.99
        )

    def test_return_empty_list_when_nothing_was_found(
        self, mocked_find_similar_images_using_id: MagicMock
    ) -> None:
        img_id = "123123"
        mocked_find_similar_images_using_id.return_value = []

        response = client.get(f"/v1/similar/{img_id}")

        assert response.status_code == 200
        assert response.json() == {
            "id": img_id,
            "similar_images": [],
        }
        mocked_find_similar_images_using_id.assert_called_once_with(
            img_id, limit=10, precision=0.99
        )
