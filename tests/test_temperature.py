
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_temperature_endpoint(monkeypatch):
    # Mock the fetch_sensebox_data function
    async def mock_fetch_sensebox_data(box_id: str):
        return {
            "sensors": [
                {
                    "title": "Temperatur",
                    "lastMeasurement": {"value": "12.34"}
                }
            ]
        }

    monkeypatch.setattr(
        "app.api.temperature.fetch_sensebox_data",
        mock_fetch_sensebox_data
    )

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/temperature")

    assert response.status_code == 200
    assert response.json()["temperature"] == pytest.approx(12.34)
