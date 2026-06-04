import httpx
import time
from datetime import datetime, timedelta, timezone

from app.metrics import (
    sensebox_fetch_total,
    sensebox_fetch_failures,
    sensebox_response_time
)


async def fetch_sensebox_data(box_id: str):
    start_time = time.time()

    url = f"https://api.opensensemap.org/boxes/{box_id}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()

            # Record success
            sensebox_fetch_total.labels(box_id=box_id, status='success').inc()
            
            return response.json()
        
    except Exception:
        # Record failure
        sensebox_fetch_total.labels(box_id=box_id, status='failure').inc()
        sensebox_fetch_failures.labels(box_id=box_id).inc()
        raise

    finally:
        # Record response time
        duration = time.time() - start_time
        sensebox_response_time.labels(box_id=box_id).observe(duration)



def extract_recent_temperatures(data: dict):
    now = datetime.now(timezone.utc)
    one_hour_ago = now - timedelta(hours=1)

    temps = []
    for sensor in data.get("sensors", []):

        if not is_temperature_sensor(sensor):
            continue
        measurement = sensor.get("lastMeasurement")

        if not measurement:
            continue

        ts = measurement.get("createdAt")
        if not ts:
            continue

        timestamp = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        if timestamp < one_hour_ago:
            continue

        value = float(measurement["value"])
        temps.append(value)

    return temps


def is_temperature_sensor(sensor):
    title = sensor["title"].lower()
    return any(
        keyword in title
        for keyword in [
            "temp",
            "temperatur",
            "temperature",
            "tmp"
        ]
    )
