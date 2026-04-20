from fastapi import APIRouter
from app.services.sensebox import fetch_sensebox_data
from app.services.sensebox import extract_recent_temperatures
from app.core.config import settings
router = APIRouter()


@router.get("/temperature")
async def temperature():
    temps = []

    for box_id in settings.sensebox_ids:
        data = await fetch_sensebox_data(box_id)
        temps.extend(extract_recent_temperatures(data))

    if not temps:
        return {"temperature": None}
    return {"temperature": sum(temps) / len(temps)}
