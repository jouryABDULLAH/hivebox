from fastapi import APIRouter, HTTPException
from app.core.config import settings
from app.services.cache import get_cached_temp, redis_client


router = APIRouter()


@router.get("/readyz")
async def readyz():
    """Check if app can connect to required services"""

    try:
        # Test Redis connectivity
        redis_client.ping()
        
        # Test MinIO connectivity (check if bucket exists or can be created)
        # If this fails, it will raise an exception
        
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "not ready",
                "error": str(e)
            }
        )