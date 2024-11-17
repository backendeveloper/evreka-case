from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class LocationData(Base):
    __tablename__ = "location_data"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    speed = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
