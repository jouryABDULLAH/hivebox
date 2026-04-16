
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from datetime import datetime, timedelta, timezone


@pytest.mark.asyncio
async def test_temperature_single_box(monkeypatch):
    now = datetime.now(timezone.utc)
    fresh = (now - timedelta(minutes=10)).isoformat()

    async def mock_fetch(box_id):
        return {
            "sensors": [
                {
                    "title": "Temperatur",
                    "unit": "°C",
                    "lastMeasurement": {
                        "value": "15.34",
                        "createdAt": fresh
                    }
                }
            ]
        }

    monkeypatch.setattr(
        "app.api.temperature.fetch_sensebox_data",
        mock_fetch
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/temperature")

    assert response.status_code == 200
    assert response.json()["temperature"] == pytest.approx(15.34)


@pytest.mark.asyncio
async def test_temperature_multiple_boxes(monkeypatch):
    now = datetime.now(timezone.utc)
    fresh = (now - timedelta(minutes=5)).isoformat()

    async def mock_fetch(box_id):
        if box_id == "A":
            return {
                "sensors": [
                    {
                        "title": "Temperatur",
                        "unit": "°C",
                        "lastMeasurement": {
                            "value": "10.0",
                            "createdAt": fresh
                        }
                    }
                ]
            }
        else:
            return {
                "sensors": [
                    {
                        "title": "Temperatur",
                        "unit": "°C",
                        "lastMeasurement": {
                            "value": "20.0",
                            "createdAt": fresh
                        }
                    }
                ]
            }

    monkeypatch.setattr(
        "app.api.temperature.fetch_sensebox_data",
        mock_fetch
    )

    from app.core.config import settings
    original = settings.SENSEBOX_IDS
    settings.SENSEBOX_IDS = "A,B"

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/temperature")

    settings.SENSEBOX_IDS = original

    assert response.status_code == 200
    assert response.json()["temperature"] == pytest.approx(15.0)


@pytest.mark.asyncio
async def test_temperature_stale_data(monkeypatch):
    now = datetime.now(timezone.utc)
    stale = (now - timedelta(hours=5)).isoformat()

    async def mock_fetch(box_id):
        return {
            "sensors": [
                {
                    "title": "Temperatur",
                    "unit": "°C",
                    "lastMeasurement": {
                        "value": "15.34",
                        "createdAt": stale
                    }
                }
            ]
        }

    monkeypatch.setattr(
        "app.api.temperature.fetch_sensebox_data",
        mock_fetch
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/temperature")

    assert response.status_code == 200
    assert response.json()["temperature"] is None


@pytest.mark.asyncio
async def test_temperature_no_temp_sensor(monkeypatch):
    async def mock_fetch(box_id):
        return {
            "sensors": [
                {
                    "title": "PM10",
                    "lastMeasurement": {
                        "value": "100",
                        "createdAt": "2026-04-15T08:55:42.309Z"
                    }
                }
            ]
        }

    monkeypatch.setattr(
        "app.api.temperature.fetch_sensebox_data",
        mock_fetch
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/temperature")

    assert response.json()["temperature"] is None
