from typing import TYPE_CHECKING, Any, BinaryIO

import boto3
from botocore import exceptions


if TYPE_CHECKING:
    from mypy_boto3_s3.type_defs import (
        DeleteObjectOutputTypeDef,
        HeadObjectOutputTypeDef,
        PutObjectOutputTypeDef,
        S3Client,
    )
else:
    DeleteObjectOutputTypeDef = dict
    HeadObjectOutputTypeDef = dict
    PutObjectOutputTypeDef = dict
    S3Client = dict

from config import AWS_ACCESS_KEY_ID, AWS_ENDPOINT_URL, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME


class S3:
    @classmethod
    def _s3(cls) -> S3Client:
        if AWS_ENDPOINT_URL.value:
            return boto3.client(
                "s3",
                endpoint_url=AWS_ENDPOINT_URL.value,
                aws_access_key_id=AWS_ACCESS_KEY_ID.value,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY.value,
            )
        return boto3.client("s3")

    @classmethod
    def create_bucket(cls) -> None:
        cls._s3().create_bucket(Bucket=S3_BUCKET_NAME.value)

    @classmethod
    def generate_presigned_get(cls, key: str, expiration: int = 3600) -> str | None:
        if cls.object_exists(key):
            return cls._s3().generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": S3_BUCKET_NAME.value, "Key": key},
                ExpiresIn=expiration,
            )
        return None

    @classmethod
    def create_img_link(cls, img_id: str, img_format) -> str | None:
        return cls.generate_presigned_get(f"{img_id}.{img_format}")

    @classmethod
    def delete_object(cls, key: str) -> DeleteObjectOutputTypeDef:
        return cls._s3().delete_object(Bucket=S3_BUCKET_NAME.value, Key=key)

    @classmethod
    def get_object(cls, key: str) -> bytes:
        return cls._s3().get_object(Bucket=S3_BUCKET_NAME.value, Key=key)["Body"].read()

    @classmethod
    def get_head(cls, key: str) -> HeadObjectOutputTypeDef:
        return cls._s3().head_object(Bucket=S3_BUCKET_NAME.value, Key=key)

    @classmethod
    def object_exists(cls, key: str) -> bool:
        try:
            cls.get_head(key)
        except exceptions.ClientError as error:
            if error.response["Error"]["Code"] == "404":
                return False
            raise error
        return True

    @classmethod
    def put_object(cls, key: str, body: bytes | BinaryIO, **kwargs: Any) -> PutObjectOutputTypeDef:
        body.seek(0)
        return cls._s3().put_object(Bucket=S3_BUCKET_NAME.value, Key=key, Body=body, **kwargs)
