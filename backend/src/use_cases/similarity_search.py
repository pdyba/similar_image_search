from numpy import ndarray, reshape
from PIL import Image

from db.milvus import MilvusConnector
from image_encoder import get_image_embedding
from storage import S3


def find_similar_images_using_image() -> list[dict]:
    milvus_client = MilvusConnector()

    with open("../backend/test_images/z00.png", "rb") as file:
        uploaded_img = Image.open(file)

    width, height = uploaded_img.size

    new_width = 370
    new_height = int((new_width / width) * height)
    uploaded_img = uploaded_img.resize((new_width, new_height))

    results = milvus_client.get_search_results_from_vector(
        query_vector=get_image_embedding(uploaded_img)
    )
    return results


def find_similar_images_using_id(
    img_id: str, limit: int, precision: float = 0.99
) -> list[dict] | None:
    milvus_client = MilvusConnector()
    if not (image := milvus_client.get_by_id(img_id)):
        return None
    vector: ndarray = reshape(image[0]["vector"], newshape=(1, -1)).flatten()

    results = milvus_client.get_search_results_from_vector(
        query_vector=vector, limit=limit, precision=precision
    )
    return [_build_data(img) for img in results[0]]


def _build_data(img: dict) -> dict:
    return {
        "id": img["id"],
        "url": S3.create_img_link(img["id"], img["entity"]["file_format"]),
        "similarity_score": round(img["distance"] * 100, 6),
    }
