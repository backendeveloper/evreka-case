from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LocationData(Base):
    __tablename__ = "location_data"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    speed = Column(Float, nullable=False)
    timestamp = Column(DateTime, index=True, nullable=False)

    __table_args__ = (
        Index('idx_device_timestamp', 'device_id', 'timestamp'),
    )