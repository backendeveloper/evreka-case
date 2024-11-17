import logging
from fastapi import FastAPI, HTTPException
from app.models import LocationData
from app.rabbitmq import publish_to_queue
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Gateway API")


@app.post("/data")
async def send_data(data: LocationData):
    try:
        message = data.model_dump(mode='json')
        publish_to_queue(settings.rabbitmq_queue, message)
        logger.info(f"Data sent to RabbitMQ: {data.dict()}")
        return {"message": "Data successfully sent to RabbitMQ"}
    except Exception as e:
        logger.error(f"Error sending data to RabbitMQ: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error sending data to RabbitMQ: {str(e)}")
