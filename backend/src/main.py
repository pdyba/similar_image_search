import logging

from api import routes
from config import API_VERSION, REDIS_HOST, REDIS_PORT
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import caches, close_caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend

logger = logging.getLogger(__name__)


tags_metadata = [
    {
        "name": "health",
        "description": "Health check for api",
    }
]

app = FastAPI(
    title="img-api",
    description="Image similarities finder",
    # version=API_VERSION.value,
    # openapi_url=f"/{API_VERSION.value}/openapi.json",
    # openapi_tags=tags_metadata,
)


@app.on_event("startup")
def on_startup() -> None:
    redis_client = RedisCacheBackend(f"{REDIS_HOST.value}:{REDIS_PORT.value}")
    caches.set(CACHE_KEY, redis_client)
    logger.info("FastAPI app running...")


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await close_caches()


app.add_middleware(CORSMiddleware, allow_origins=["*"])

app.include_router(routes.api_router, prefix=f"/{API_VERSION.value}")
