import pytest
from datetime import datetime, timedelta
from httpx import AsyncClient
from app.db.models import LocationData

from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_get_locations(async_client: AsyncClient, db_session: AsyncSession):
    now = datetime.utcnow()
    location = LocationData(
        device_id="device123",
        latitude=40.7128,
        longitude=-74.0060,
        speed=60.5,
        timestamp=now
    )
    db_session.add(location)
    await db_session.commit()

    start_date = (now - timedelta(days=1)).isoformat()
    end_date = (now + timedelta(days=1)).isoformat()
    response = await async_client.get(
        "/analytics/getlocation",
        params={
            "start_date": start_date,
            "end_date": end_date,
            "limit": 10,
            "offset": 0
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["device_id"] == "device123"
