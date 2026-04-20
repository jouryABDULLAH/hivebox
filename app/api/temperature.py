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
    status = ''

    if not temps:
        return {"temperature": None, "status": status}
    
    average_tmp = sum(temps) / len(temps)
    average_tmp = round(average_tmp, 2)
    status = classify_temperature(average_tmp)
    return {"temperature": average_tmp,"status": status}


def classify_temperature(temp: float) -> str:
    if temp < 10:
        return "Too Cold"
    elif 10 <= temp <= 36:
        return "Good"
    else:
        return "Too Hot"
