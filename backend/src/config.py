import logging

from dotenv import load_dotenv
from lbz.configuration import ConfigParser, EnvValue

load_dotenv()

COLLECTION_NAME = EnvValue[str]("COLLECTION_NAME")
MILVUS_ENDPOINT = EnvValue[str]("MILVUS_ENDPOINT")
MILVUS_TOKEN = EnvValue[str | None]("MILVUS_TOKEN", default="")
MODEL_NAME = EnvValue[str]("MODEL_NAME")
MODEL_DIM = EnvValue[str]("MODEL_DIM")

ACCESS_TOKEN_EXPIRE_MINUTES = EnvValue[int]("ACCESS_TOKEN_EXPIRE_MINUTES", default=60 * 24 * 8)
# SERVER_NAME: Optional[str] = Field(..., env="NGINX_HOST")
BACKEND_CORS_ORIGINS = EnvValue[list[str]](
    "MODEL_DIM", default=["*"], parser=ConfigParser.split_by_comma
)
LOG_LEVEL = EnvValue[int]("LOG_LEVEL", default=logging.INFO)

VERSION = EnvValue[str]("VERSION")
API_VERSION = EnvValue[str]("API_VERSION", default="v1")
DEBUG = EnvValue[bool]("DEBUG", default=True)

REDIS_HOST = EnvValue[str]("REDIS_HOST")
REDIS_PORT = EnvValue[str]("REDIS_PORT")

WEB_CONCURRENCY = EnvValue[int]("WEB_CONCURRENCY", default=9)
MAX_OVERFLOW = EnvValue[int]("MAX_OVERFLOW", default=64)

# AWS
S3_BUCKET_NAME = EnvValue[str]("S3_BUCKET_NAME")
AWS_ACCESS_KEY_ID = EnvValue[str]("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = EnvValue[str]("AWS_SECRET_ACCESS_KEY")
AWS_ENDPOINT_URL = EnvValue[str]("AWS_ENDPOINT_URL")
