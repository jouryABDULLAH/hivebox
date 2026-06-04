from redis import Redis
from typing import Optional
from app.core.config import settings
from app.metrics import cache_operations

redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)


def get_cached_temp(box_id: str) -> Optional[str]:

    try: 
        result = redis_client.get(f"temp:{box_id}")
        if result:
            cache_operations.labels(operation='get', status='hit').inc()
        else:
            cache_operations.labels(operation='get', status='miss').inc()
            
        return result if isinstance(result, str) else None
    except Exception:
        cache_operations.labels(operation='get', status='error')
        raise


def cache_temp(box_id: str, temp: float, ttl: int = 300) -> None:
    try:
        redis_client.setex(f"temp:{box_id}", ttl, str(temp))
        cache_operations.labels(operation='set', status='success').inc()
    except Exception:
        cache_operations.labels(operation='set', status='error').inc()
        raise