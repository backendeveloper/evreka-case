from pydantic import BaseModel, Field
from datetime import datetime

class LocationData(BaseModel):
    device_id: str = Field(..., description="DeviceId")
    latitude: float = Field(..., description="Latitude")
    longitude: float = Field(..., description="Longitude")
    speed: float = Field(..., description="Speed")
    timestamp: datetime = Field(..., description="DateTime")