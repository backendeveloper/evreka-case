from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from datetime import datetime
from app.db.models import LocationData
from app.db.session import get_db
from app.schemas.response_schemas import LocationDataResponse

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
    responses={404: {"description": "Not found"}}
)

@router.get("/getlocation", response_model=List[LocationDataResponse])
async def get_locations(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date must be before end_date.")

    query_stmt = select(LocationData).where(
        LocationData.timestamp >= start_date,
        LocationData.timestamp <= end_date
    ).order_by(LocationData.timestamp.desc()).offset(offset).limit(limit)

    result = await db.execute(query_stmt)
    data = result.scalars().all()
    if not data:
        raise HTTPException(status_code=404, detail="No data found for the specified date range.")
    return data

@router.get("/getdevice")
async def get_device(
    device_id: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    query_stmt = select(LocationData).where(
        LocationData.device_id == device_id
    ).order_by(LocationData.timestamp.desc()).limit(1)
    result = await db.execute(query_stmt)
    data = result.scalar_one_or_none()
    if data is None:
        raise HTTPException(status_code=404, detail="No data found for the specified device.")
    return data