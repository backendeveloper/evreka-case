import pytest
import json
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from app.db.models import LocationData
from app.rabbitmq.consumer import on_message
from sqlalchemy.ext.asyncio import AsyncSession
from aio_pika import IncomingMessage


@pytest.mark.asyncio
async def test_save_to_db(mocker, db_session: AsyncSession):
    mock_add = mocker.spy(db_session, "add")
    mock_commit = mocker.spy(db_session, "commit")

    message = {
        "device_id": "device123",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "speed": 60.5,
        "timestamp": datetime.utcnow().isoformat()
    }

    from app.rabbitmq.consumer import save_to_db
    await save_to_db(message, db_session)

    assert mock_add.call_count == 1, "session.add() should be called once"
    added_instance = mock_add.call_args.args[0]
    assert isinstance(added_instance, LocationData), "Added instance should be LocationData"
    assert added_instance.device_id == message["device_id"]
    assert added_instance.latitude == message["latitude"]
    assert added_instance.longitude == message["longitude"]
    assert added_instance.speed == message["speed"]
    assert added_instance.timestamp.isoformat() == message["timestamp"]

    assert mock_commit.call_count == 1, "session.commit() should be called once"


@pytest.mark.asyncio
async def test_on_message_success(mocker, db_session: AsyncSession):
    mock_save_to_db = mocker.patch("app.rabbitmq.consumer.save_to_db", new=AsyncMock())

    mock_message = MagicMock(spec=IncomingMessage)
    mock_message.body = json.dumps({
        "device_id": "device123",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "speed": 60.5,
        "timestamp": datetime.utcnow().isoformat()
    }).encode('utf-8')

    mock_process = MagicMock()
    mock_process.__aenter__ = AsyncMock(return_value=None)
    mock_process.__aexit__ = AsyncMock(return_value=None)
    mock_message.process = MagicMock(return_value=mock_process)

    await on_message(mock_message, db_session)

    mock_save_to_db.assert_awaited_once_with({
        "device_id": "device123",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "speed": 60.5,
        "timestamp": mocker.ANY
    }, db_session)


@pytest.mark.asyncio
async def test_on_message_failure_invalid_json(mocker, db_session: AsyncSession):
    mock_save_to_db = mocker.patch("app.rabbitmq.consumer.save_to_db", new=AsyncMock())

    mock_message = MagicMock(spec=IncomingMessage)
    mock_message.body = b"invalid json"

    mock_process = MagicMock()
    mock_process.__aenter__ = AsyncMock(return_value=None)
    mock_process.__aexit__ = AsyncMock(return_value=None)
    mock_message.process = MagicMock(return_value=mock_process)

    mock_logger = mocker.patch("app.rabbitmq.consumer.logger.error")

    await on_message(mock_message, db_session)

    mock_save_to_db.assert_not_called()

    mock_logger.assert_called_once()


@pytest.mark.asyncio
async def test_on_message_failure_save_to_db_exception(mocker, db_session: AsyncSession):
    mock_save_to_db = mocker.patch("app.rabbitmq.consumer.save_to_db",
                                   new=AsyncMock(side_effect=Exception("Test Exception")))

    mock_message = MagicMock(spec=IncomingMessage)
    mock_message.body = json.dumps({
        "device_id": "device123",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "speed": 60.5,
        "timestamp": datetime.utcnow().isoformat()
    }).encode('utf-8')

    mock_process = MagicMock()
    mock_process.__aenter__ = AsyncMock(return_value=None)
    mock_process.__aexit__ = AsyncMock(return_value=None)
    mock_message.process = MagicMock(return_value=mock_process)

    mock_logger = mocker.patch("app.rabbitmq.consumer.logger.error")

    await on_message(mock_message, db_session)

    mock_save_to_db.assert_awaited_once_with({
        "device_id": "device123",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "speed": 60.5,
        "timestamp": mocker.ANY
    }, db_session)

    mock_logger.assert_called_once()
