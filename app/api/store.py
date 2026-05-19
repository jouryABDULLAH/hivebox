from fastapi import APIRouter
from app.services.sensebox import fetch_sensebox_data
from app.services.sensebox import extract_recent_temperatures
from app.services.storage import store_sensor_data
from app.core.config import settings

router = APIRouter()


@router.get("/store")
async def store():
    # Fetch current data and store to MinIO
    all_data = {}
    for box_id in settings.sensebox_ids:
        data = await fetch_sensebox_data(box_id)
        temps = extract_recent_temperatures(data)
        all_data[box_id] = temps
    store_sensor_data(all_data)
    return {"status": "stored"}