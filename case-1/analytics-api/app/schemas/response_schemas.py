from pydantic import BaseModel
from datetime import datetime


class LocationDataResponse(BaseModel):
    id: int
    device_id: str
    latitude: float
    longitude: float
    speed: float
    timestamp: datetime

    class Config:
        orm_mode = True
