import asyncio
import logging
from fastapi import FastAPI
from app.db.session import init_db
from app.rabbitmq.consumer import consume

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Worker API",
    description="Worker API",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    await init_db()
    logger.info("Database tables created.")

    asyncio.create_task(consume())
    logger.info("RabbitMQ consumer started.")