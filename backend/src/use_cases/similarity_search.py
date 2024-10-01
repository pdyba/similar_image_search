from PIL import Image
from numpy import reshape, ndarray
from image_encoder import get_image_embedding
from db.milvus import MilvusConnector
from storage import S3


def find_similar_images_using_image():
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


def find_similar_images_using_id(img_id: str):
    milvus_client = MilvusConnector()
    image = milvus_client.get_by_id(img_id)
    if not image:
        return None
    vector: ndarray = reshape(image[0]["vector"], newshape=(1, -1)).flatten()

    results = milvus_client.get_search_results_from_vector(query_vector=vector)
    return [_build_data(img) for img in results[0]]


def _build_data(img: dict) -> dict:
    return {
        "id": img["id"],
        "url": S3.create_img_link(img["id"], img["entity"]["file_format"]),
        "similarity_score": round(img["distance"] * 100, 6),
    }
