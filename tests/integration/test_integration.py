# verify the endpoint responds correctly by calling the real OpensMapSenseAPI

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# /version integration is covered by unit tests (test_version.py)
# since it has no external dependencies, unit testing is sufficient


def test_temperature_integration():
    response = client.get("/temperature")
    assert response.status_code == 200
    assert "temperature" in response.json()
    assert "status" in response.json()


def test_metrics_integration():
    response = client.get("/metrics")
    assert response.status_code == 200