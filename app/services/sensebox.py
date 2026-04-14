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
        temps = [
            float(sensor["lastMeasurement"]["value"])    
            for sensor in data["sensors"]    
            if is_temperature_sensor(sensor)
        ]
    return temps

def is_temperature_sensor(sensor):
    title = sensor["title"].lower()
    return any(keyword in title for keyword in ["temp", "temperatur", "temperature", "tmp"])
