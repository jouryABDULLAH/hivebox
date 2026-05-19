from fastapi import APIRouter, HTTPException
from app.core.config import settings
from app.services.cache import get_cached_temp


router = APIRouter()


@router.get("/readyz")
async def readyz():
    box_ids = settings.sensebox_ids
    total = len(box_ids)
    required = (total // 2) + 1   # 50% + 1

    accessible = 0
    
    for box_id in box_ids:
        cached = get_cached_temp(box_id)

        # If cached exists → box is accessible 
        # AND cache is fresh (<5 min) since cache keeps data only for 5min
        if cached is not None:
            accessible += 1

    if accessible >= required:
        return {"status": "ready"}  # FastAPI automatically returns HTTP 200

    raise HTTPException(
        status_code=503,
        detail={
            "status": "not ready",
            "accessible_boxes": accessible,
            "required": required
        }
    )