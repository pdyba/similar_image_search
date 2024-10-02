from unittest.mock import MagicMock, patch

from db import MilvusConnector
from pymilvus import MilvusClient, MilvusException


class TestMilvusConnector:
    @patch.object(MilvusClient, "search", autospec=True)
    def test__get_search_results_from_vector__calls_search_with_default_values(
        self, mocked_search: MagicMock
    ) -> None:
        mocked_search.return_value = []
        query_vector = [1, 2, 3]

        MilvusConnector().get_search_results_from_vector(query_vector)

        mocked_search.assert_called_once_with(
            collection_name="images",
            data=[query_vector],
            search_params={
                "metric_type": "COSINE",
                "params": {
                    "nprobe": 20,  # number of partitions to search
                    "radius": 0.6,  # Only consider vectors with similarity >= x
                    "range_filter": 0.99,  # Return results with similarity >= y
                },
            },
            output_fields=["vector", "file_format"],
            limit=10,
        )

    @patch.object(MilvusClient, "get", autospec=True)
    def test__get_by_id__calls_get_with_default_values(self, mocked_get: MagicMock) -> None:
        mocked_get.return_value = []
        img_id = "123"

        MilvusConnector().get_by_id(img_id)

        mocked_get.assert_called_once_with(
            collection_name="images",
            ids=img_id,
            output_fields=["vector", "file_format"],
        )
