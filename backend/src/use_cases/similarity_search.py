from db.milvus import MilvusConnector
from numpy import ndarray, reshape
from storage import S3


def find_similar_images_using_id(
    img_id: str, limit: int = 10, precision: float = 0.99
) -> list[dict] | None:
    milvus_client = MilvusConnector()
    if not (image := milvus_client.get_by_id(img_id)):
        return None
    vector: ndarray = reshape(image[0]["vector"], newshape=(1, -1)).flatten()

    results = milvus_client.get_search_results_from_vector(
        query_vector=vector, limit=limit, precision=precision
    )
    return [_build_data(img) for img in results]


def _build_data(img: dict) -> dict:
    return {
        "id": img["id"],
        "url": S3.create_img_link(img["id"], img["entity"]["file_format"]),
        "similarity_score": round(img["distance"] * 100, 6),
    }
