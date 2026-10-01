import pytest
from httpx import AsyncClient

# Simple tests requiring running backend at localhost:8000

@pytest.mark.asyncio
async def test_get_plants():
    async with AsyncClient(base_url="http://localhost:8000", headers={"Authorization": "Bearer MOCK_TOKEN_ADMIN"}) as ac:
        response = await ac.get("/v1/hierarchy/plants")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_timeseries():
    async with AsyncClient(base_url="http://localhost:8000", headers={"Authorization": "Bearer MOCK_TOKEN_ADMIN"}) as ac:
        response = await ac.get("/v1/energy/timeseries")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_distribution():
    async with AsyncClient(base_url="http://localhost:8000", headers={"Authorization": "Bearer MOCK_TOKEN_ADMIN"}) as ac:
        response = await ac.get("/v1/energy/distribution")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_production_timeseries():
    async with AsyncClient(base_url="http://localhost:8000", headers={"Authorization": "Bearer MOCK_TOKEN_ADMIN"}) as ac:
        response = await ac.get("/v1/production/timeseries")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_production_intensity():
    async with AsyncClient(base_url="http://localhost:8000", headers={"Authorization": "Bearer MOCK_TOKEN_ADMIN"}) as ac:
        response = await ac.get("/v1/production/intensity")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_cost_breakdown():
    async with AsyncClient(base_url="http://localhost:8000", headers={"Authorization": "Bearer MOCK_TOKEN_ADMIN"}) as ac:
        response = await ac.get("/v1/cost/breakdown")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_post_ai_chat():
    async with AsyncClient(base_url="http://localhost:8000", headers={"Authorization": "Bearer MOCK_TOKEN_ADMIN"}) as ac:
        response = await ac.post("/v1/ai/chat", json={"message": "Anomaly"})
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data

@pytest.mark.asyncio
async def test_get_ai_anomalies():
    async with AsyncClient(base_url="http://localhost:8000", headers={"Authorization": "Bearer MOCK_TOKEN_ADMIN"}) as ac:
        response = await ac.get("/v1/ai/anomalies")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "severity" in data[0]

@pytest.mark.asyncio
async def test_get_ai_forecast():
    async with AsyncClient(base_url="http://localhost:8000", headers={"Authorization": "Bearer MOCK_TOKEN_ADMIN"}) as ac:
        response = await ac.get("/v1/ai/forecast")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "predicted_kwh" in data[0]
