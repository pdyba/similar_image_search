import logging

from config import COLLECTION_NAME, MILVUS_ENDPOINT, MILVUS_TOKEN, MODEL_DIM
from numpy import array, ndarray
from pymilvus import MilvusClient, MilvusException

DEFAULT_OUTPUT_FIELDS = ["vector", "file_format"]
logger = logging.getLogger(__name__)


class MilvusConnector:
    def __init__(self) -> None:
        self._milvus_client = None

    @property
    def milvus_client(self) -> MilvusClient:
        if self._milvus_client is None:
            self._milvus_client = MilvusClient(uri=MILVUS_ENDPOINT.value, token=MILVUS_TOKEN.value)
        return self._milvus_client

    def create_collection(self, drop_old: bool | None = None) -> None:
        if self.milvus_client.has_collection(COLLECTION_NAME.value) and drop_old:
            self.milvus_client.drop_collection(COLLECTION_NAME.value)
        if self.milvus_client.has_collection(COLLECTION_NAME.value):
            if drop_old is False:
                raise RuntimeError(
                    f"Collection {COLLECTION_NAME.value} already exists. "
                    f"Set drop_old=True to create a new one instead."
                )
            return None
        self.milvus_client.create_collection(
            collection_name=COLLECTION_NAME.value,
            dimension=MODEL_DIM.value,
            metric_type="COSINE",
            consistency_level="Strong",
            auto_id=False,
        )

    def get_search_results_from_vector(
        self,
        query_vector: array | ndarray,
        output_fields: list | None = None,
        limit: int = 10,
        precision: float = 0.99,
    ) -> list[dict]:
        return self.milvus_client.search(
            collection_name=COLLECTION_NAME.value,
            data=[query_vector],
            search_params={
                "metric_type": "COSINE",
                "params": {
                    "nprobe": 20,  # number of partitions to search
                    "radius": 0.6,  # Only consider vectors with similarity >= x
                    "range_filter": precision,  # Return results with similarity >= y
                },
            },
            output_fields=output_fields or DEFAULT_OUTPUT_FIELDS,
            limit=limit,
        )[0]

    def insert(self, data: dict) -> dict | list:
        return self.milvus_client.insert(
            collection_name=COLLECTION_NAME.value,
            data=data,
        )

    def get_by_id(self, img_id: str, output_fields: list | None = None) -> dict | list:
        return self.milvus_client.get(
            collection_name=COLLECTION_NAME.value,
            ids=img_id,
            output_fields=output_fields or DEFAULT_OUTPUT_FIELDS,
        )

    def get_collection_stats(self) -> dict | None:
        try:
            return self.milvus_client.get_collection_stats(collection_name=COLLECTION_NAME.value)
        except MilvusException:
            return
