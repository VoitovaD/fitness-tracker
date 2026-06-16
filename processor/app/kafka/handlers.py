import json
import logging

logger = logging.getLogger(__name__)

async def handle_message(msg):
    try:
        key = msg.key.decode("utf-8") if msg.key else None
        value = json.loads(msg.value.decode("utf-8"))
        logger.info(f"Processing message key={key} value={value}")

    except Exception as e:
        logger.error(f"Error handling message: {e}")