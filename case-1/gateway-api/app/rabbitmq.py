import pika
import json
from app.core.config import settings


def get_connection():
    credentials = pika.PlainCredentials(settings.rabbitmq_user, settings.rabbitmq_password)
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.rabbitmq_host,
            port=settings.rabbitmq_port,
            credentials=credentials
        )
    )


def publish_to_queue(queue_name, message: dict):
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    message_body = json.dumps(message).encode('utf-8')
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message_body,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()
