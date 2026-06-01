from fastapi import APIRouter
from app.services.sensebox import fetch_sensebox_data
from app.services.sensebox import extract_recent_temperatures
from app.core.config import settings
from app.services.cache import cache_temp
from app.services.cache import get_cached_temp
import time
from app.metrics import (
    current_temperature,
    accessible_boxes,
    temperature_fetch_duration
)

router = APIRouter()


@router.get("/temperature")
async def temperature():
    start_time = time.time()

    temps = []
    accessible_count = 0


    for box_id in settings.sensebox_ids:
        # Check cache
        cached = get_cached_temp(box_id)
        if cached is not None:
            temps.append(float(cached))
            accessible_count += 1
            continue

        try:
            data = await fetch_sensebox_data(box_id)
            box_temps = extract_recent_temperatures(data)
            if box_temps:
                # cache_temp(box_id, box_temps[0])
                temps.extend(box_temps)
                accessible_count += 1
        except Exception:
            continue

    accessible_boxes.set(accessible_count)
    

    if not temps:
        return {"temperature": None, "status": ''}
    
    average_tmp = sum(temps) / len(temps)
    average_tmp = round(average_tmp, 2)
    current_temperature.set(average_tmp)
    status = classify_temperature(average_tmp)

    # Record duration
    duration = time.time() - start_time
    temperature_fetch_duration.observe(duration)
    
    return {"temperature": average_tmp, "status": status}


def classify_temperature(temp: float) -> str:
    if temp < 10:
        return "Too Cold"
    elif 10 <= temp <= 36:
        return "Good"
    else:
        return "Too Hot"
