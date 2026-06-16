from aiokafka import AIOKafkaConsumer
import asyncio
import logging

from app.avro_deserializer import AvroDeserializer
from config import settings
from app.kafka.handlers import handle_message

logger = logging.getLogger(__name__)


async def start_consumer():
    deserializer = AvroDeserializer(settings.SCHEMA_REGISTRY_URL)

    consumer = AIOKafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=settings.KAFKA_GROUP_ID,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )

    await consumer.start()
    logger.info(f"Consumer started, listening to '{settings.KAFKA_TOPIC}'")

    try:
        async for msg in consumer:
            try:
                event = deserializer.deserialize(msg.value)
                logger.info(f"Decoded event: {event}")
                await handle_message(event)
            except Exception as e:
                logger.error(f"Failed to deserialize message: {e}")
    except asyncio.CancelledError:
        logger.info("Consumer Cancelled Error")
    finally:
        await consumer.stop()