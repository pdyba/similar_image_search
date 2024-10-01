from typing import BinaryIO
import zlib
from PIL import Image

from image_encoder import get_image_embedding
from exceptions import UploadField

from db.milvus import MilvusConnector
from storage import S3


def upload_image(file: BinaryIO, file_format: str) -> int:
    try:
        milvus_client = MilvusConnector()
        data = prepare_image(file, file_format)

        S3.put_object(f"{data['id']}.{data['file_format']}", file)

        response = milvus_client.insert(data=data)
        if response["insert_count"] == 1:
            return data["id"]
        raise UploadField(f"Upload field: due to an error occurs during the embedding process")
    except Exception as e:
        raise UploadField(
            f"Upload field: due to an error occurs during the embedding process:\n{e}"
        ) from e


def prepare_image(file: BinaryIO, file_format: str):
    image = Image.open(file)
    image_embedding = get_image_embedding(image)
    file.seek(0)
    file_id = zlib.crc32(file.read())
    return {"id": file_id, "vector": image_embedding, "file_format": file_format}
