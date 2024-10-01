import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from api import routes
from config import API_VERSION
from db import get_redis_client


logger = logging.getLogger(__name__)


tags_metadata = [
    {
        "name": "health",
        "description": "Health check for api",
    }
]

app = FastAPI(
    title="img-api",
    description="base project for fastapi backend",
    # version=API_VERSION.value,
    # openapi_url=f"/{API_VERSION.value}/openapi.json",
    # openapi_tags=tags_metadata,
)


def on_startup() -> None:
    redis_client = get_redis_client()
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
    logger.info("FastAPI app running...")


app.add_middleware(CORSMiddleware, allow_origins=["*"])

app.add_event_handler("startup", on_startup)

app.include_router(routes.api_router, prefix=f"/{API_VERSION.value}")
