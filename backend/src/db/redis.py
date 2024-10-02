from config import REDIS_HOST, REDIS_PORT
from redis import Redis


def get_redis_client() -> Redis:
    redis = Redis.from_url(
        f"redis://{REDIS_HOST.value}:{REDIS_PORT.value}",
        max_connections=10,
        encoding="utf8",
        decode_responses=True,
    )
    return redis
