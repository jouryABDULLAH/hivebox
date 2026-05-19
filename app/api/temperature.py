from fastapi import APIRouter
from app.services.sensebox import fetch_sensebox_data
from app.services.sensebox import extract_recent_temperatures
from app.core.config import settings
from app.services.cache import cache_temp
from app.services.cache import get_cached_temp

router = APIRouter()


@router.get("/temperature")
async def temperature():
    temps = []
    print("Connecting to Redis:", settings.REDIS_HOST, settings.REDIS_PORT)

    for box_id in settings.sensebox_ids:


        # Check cache
        cached = get_cached_temp(box_id)
        if cached is not None:
            temps.append(float(cached))
            continue

        # If not cached, fetch and cache
        data = await fetch_sensebox_data(box_id)
        box_temps = extract_recent_temperatures(data)
        if box_temps:
            # cache_temp(box_id, box_temps[0])
            temps.extend(box_temps)


    status = ''

    if not temps:
        return {"temperature": None, "status": status}
    average_tmp = sum(temps) / len(temps)
    average_tmp = round(average_tmp, 2)
    status = classify_temperature(average_tmp)
    return {"temperature": average_tmp, "status": status}


def classify_temperature(temp: float) -> str:
    if temp < 10:
        return "Too Cold"
    elif 10 <= temp <= 36:
        return "Good"
    else:
        return "Too Hot"
