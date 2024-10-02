from unittest.mock import ANY, MagicMock, call, patch

from db import MilvusConnector
from numpy import array
from numpy.testing import assert_array_equal
from storage import S3
from use_cases import find_similar_images_using_id


@patch.object(S3, "create_img_link", autospec=True)
@patch.object(MilvusConnector, "get_by_id", autospec=True)
@patch.object(MilvusConnector, "get_search_results_from_vector", autospec=True)
class TestFindSimilarImagesUsingID:
    def test_returns_none_if_base_image_not_found(
        self,
        mocked_get_search_results_from_vector: MagicMock,
        mocked_get_by_id: MagicMock,
        mocked_create_img_link: MagicMock,
    ) -> None:
        mocked_get_by_id.return_value = []

        images = find_similar_images_using_id("123123")

        assert images is None
        mocked_get_by_id.assert_called_once_with(ANY, "123123")
        mocked_get_search_results_from_vector.assert_not_called()
        mocked_create_img_link.assert_not_called()

    def test_returns_empty_list_when_no_similar_images_were_found(
        self,
        mocked_get_search_results_from_vector: MagicMock,
        mocked_get_by_id: MagicMock,
        mocked_create_img_link: MagicMock,
    ) -> None:
        img_id = "123123"
        vector = [1, 2, 3]
        mocked_get_by_id.return_value = [{"id": img_id, "vector": vector, "file_format": "png"}]
        mocked_get_search_results_from_vector.return_value = [[]]

        images = find_similar_images_using_id(img_id)

        assert images == []
        mocked_get_by_id.assert_called_once_with(ANY, "123123")
        mocked_get_search_results_from_vector.assert_called_once_with(
            ANY, query_vector=ANY, limit=10, precision=0.99
        )
        assert_array_equal(
            array(vector), mocked_get_search_results_from_vector.call_args[1]["query_vector"]
        )
        mocked_create_img_link.assert_not_called()

    def test_returns_response_formated_as_expected(
        self,
        mocked_get_search_results_from_vector: MagicMock,
        mocked_get_by_id: MagicMock,
        mocked_create_img_link: MagicMock,
    ) -> None:
        img_id = "123123"
        vector = [1, 2, 3]
        vector_s1 = [9, 9, 9]
        vector_s2 = [4, 4, 4]
        mocked_get_by_id.return_value = [{"id": img_id, "vector": vector, "file_format": "png"}]
        mocked_get_search_results_from_vector.return_value = [
            [
                {
                    "id": "x",
                    "distance": 0.98123456789,
                    "entity": {"vector": vector_s1, "file_format": "png"},
                },
                {
                    "id": "z",
                    "distance": 0.92987654321,
                    "entity": {"vector": vector_s2, "file_format": "jpg"},
                },
            ]
        ]
        mocked_create_img_link.side_effect = ["link_1", "link_2"]

        images = find_similar_images_using_id(img_id)

        assert images == [
            {"id": "x", "similarity_score": 98.123457, "url": "link_1"},
            {"id": "z", "similarity_score": 92.987654, "url": "link_2"},
        ]
        mocked_get_by_id.assert_called_once_with(ANY, "123123")
        mocked_get_search_results_from_vector.assert_called_once_with(
            ANY, query_vector=ANY, limit=10, precision=0.99
        )
        assert_array_equal(
            array(vector), mocked_get_search_results_from_vector.call_args[1]["query_vector"]
        )
        assert mocked_create_img_link.call_args_list == [
            call("x", "png"),
            call("z", "jpg"),
        ]
