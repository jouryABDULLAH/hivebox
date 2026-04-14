import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.config import settings



@pytest.mark.asyncio
async def test_version_endpoint():
    
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/version")
    assert response.status_code == 200
    assert response.json()["version"] == settings.APP_VERSION
