from fastapi import APIRouter, HTTPException
from app.services.sensebox import fetch_sensebox_data
from app.services.sensebox import extract_recent_temperatures
from app.services.storage import store_sensor_data
from app.core.config import settings

router = APIRouter()


@router.get("/store")
async def store():
    # Fetch current data and store to MinIO
    try:

        all_data = {}
        for box_id in settings.sensebox_ids:
            
            try:
                data = await fetch_sensebox_data(box_id)
                temps = extract_recent_temperatures(data)
                all_data[box_id] = temps
            except Exception as e:
                # Skip boxes that fail
                print(f"Failed to fetch {box_id}: {e}")
                continue

        store_sensor_data(all_data)
        return {"status": "stored"}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Storage failed: {str(e)}"
        )