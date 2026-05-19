from redis import Redis
from typing import Optional
from app.core.config import settings

redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)


def get_cached_temp(box_id: str) -> Optional[str]:
    result = redis_client.get(f"temp:{box_id}")
    return result if isinstance(result, str) else None


def cache_temp(box_id: str, temp: float, ttl: int = 300) -> None:
    redis_client.setex(f"temp:{box_id}", ttl, str(temp))