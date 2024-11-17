import json
import pika
import pytest
from unittest.mock import patch, MagicMock
from app.core.config import settings
from app.rabbitmq import publish_to_queue


def test_publish_to_queue_success():
    with patch("app.rabbitmq.get_connection") as mock_get_connection:
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        mock_get_connection.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel

        message = {
            "device_id": "device123",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "speed": 60.5,
            "timestamp": "2023-10-01T12:00:00"
        }

        publish_to_queue(settings.rabbitmq_queue, message)

        mock_get_connection.assert_called_once()
        mock_connection.channel.assert_called_once()
        mock_channel.queue_declare.assert_called_once_with(queue=settings.rabbitmq_queue, durable=True)
        expected_body = json.dumps(message).encode('utf-8')
        mock_channel.basic_publish.assert_called_once_with(
            exchange='',
            routing_key=settings.rabbitmq_queue,
            body=expected_body,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        mock_connection.close.assert_called_once()


def test_publish_to_queue_failure():
    with patch("app.rabbitmq.get_connection", side_effect=Exception("Connection Error")) as mock_get_connection:
        message = {
            "device_id": "device123",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "speed": 60.5,
            "timestamp": "2023-10-01T12:00:00"
        }

        with pytest.raises(Exception) as exc_info:
            publish_to_queue(settings.rabbitmq_queue, message)

        assert str(exc_info.value) == "Connection Error"
        mock_get_connection.assert_called_once()
