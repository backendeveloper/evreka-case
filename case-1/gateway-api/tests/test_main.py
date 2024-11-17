import pytest
from unittest.mock import patch
from datetime import datetime, timezone
from app.core.config import settings
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_send_data_success(async_client: AsyncClient):
    payload = {
        "device_id": "device123",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "speed": 60.5,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    with patch("app.main.publish_to_queue") as mock_publish:
        response = await async_client.post("/data", json=payload)
        assert response.status_code == 200
        assert response.json() == {"message": "Data successfully sent to RabbitMQ"}
        mock_publish.assert_called_once_with(settings.rabbitmq_queue, payload)


@patch("app.main.publish_to_queue", side_effect=Exception("RabbitMQ connection error"))
async def test_send_data_rabbitmq_failure(async_client: AsyncClient):
    payload = {
        "device_id": "device123",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "speed": 60.5,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    with patch("app.rabbitmq.publish_to_queue", side_effect=Exception("RabbitMQ connection error")) as mock_publish:
        response = await async_client.post("/data", json=payload)
        assert response.status_code == 500
        assert "Error sending data to RabbitMQ" in response.json()["detail"]
        mock_publish.assert_called_once_with(settings.rabbitmq_queue, payload)


@pytest.mark.asyncio
async def test_send_data_invalid_payload(async_client: AsyncClient):
    invalid_payload = {
        "device_id": "device123",
        "latitude": "invalid_latitude",
        "longitude": -74.0060,
        "speed": "fast"
    }

    response = await async_client.post("/data", json=invalid_payload)
    assert response.status_code == 422

    errors = response.json()["detail"]
    assert len(errors) == 3

    assert errors[0]["loc"] == ["body", "latitude"]
    assert errors[0]["type"] in ["type_error.float", "float_parsing"]

    assert errors[1]["loc"] == ["body", "speed"]
    assert errors[1]["type"] in ["type_error.float", "float_parsing"]

    assert errors[2]["loc"] == ["body", "timestamp"]
    assert errors[2]["msg"] == "Field required"
