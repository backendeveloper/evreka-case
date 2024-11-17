from app.schemas.response_schemas import LocationDataResponse
from datetime import datetime

def test_location_data_response():
    data = {
        "id": 1,
        "device_id": "device123",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "speed": 60.5,
        "timestamp": datetime.utcnow().isoformat()
    }
    schema = LocationDataResponse(**data)
    assert schema.id == data["id"]
    assert schema.device_id == data["device_id"]
    assert schema.latitude == data["latitude"]
    assert schema.longitude == data["longitude"]
    assert schema.speed == data["speed"]
    assert isinstance(schema.timestamp, datetime)