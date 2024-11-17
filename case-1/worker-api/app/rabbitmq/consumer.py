import json
import logging
import aio_pika
from datetime import datetime
from app.core.config import settings
from app.db.models import LocationData
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def save_to_db(message: dict, session: AsyncSession):
    location = LocationData(
        device_id=message["device_id"],
        latitude=message["latitude"],
        longitude=message["longitude"],
        speed=message["speed"],
        timestamp=datetime.fromisoformat(message["timestamp"])
    )
    session.add(location)
    await session.commit()
    logger.info(f"Message saved to database: {message}")


async def on_message(message: aio_pika.IncomingMessage, session: AsyncSession):
    async with message.process():
        try:
            data = json.loads(message.body.decode())
            await save_to_db(data, session)
        except Exception as e:
            logger.error(f"Error processing message: {e}")


async def consume():
    connection = await aio_pika.connect_robust(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        login=settings.rabbitmq_user,
        password=settings.rabbitmq_password
    )
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=10)

    queue = await channel.declare_queue(
        settings.rabbitmq_queue,
        durable=True
    )

    # RabbitMQ mesajlarını tüketirken get_db kullanarak oturum sağlamak
    async for message in queue:
        async for session in get_db():
            await on_message(message, session)
    logger.info("Started consuming messages.")

    return connection
