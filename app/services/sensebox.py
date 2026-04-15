import httpx
from datetime import datetime, timedelta, timezone


async def fetch_sensebox_data(box_id: str):
    url = f"https://api.opensensemap.org/boxes/{box_id}"
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
    


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
    return any(keyword in title for keyword in ["temp", "temperatur", "temperature", "tmp"])
