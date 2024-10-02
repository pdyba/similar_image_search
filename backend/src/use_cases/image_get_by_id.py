import logging

from db.milvus import MilvusConnector
from storage import S3

logger = logging.getLogger(__name__)


def get_image_by_id(img_id: str) -> dict | None:
    try:
        milvus_client = MilvusConnector()
        if not (data := milvus_client.get_by_id(img_id)):
            return None
        data = data[0]
        return {
            "id": data["id"],
            "url": S3.create_img_link(data["id"], data["file_format"]),
        }
    except Exception as e:
        logger.exception(e)
        return None
