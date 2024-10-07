from aio_pika.abc import AbstractIncomingMessage
from loguru import logger
import json

# from charge_point_node.main import OnconnectionEvent, EventName
import logging

logging.basicConfig(level=logging.INFO)


async def process_event(event: AbstractIncomingMessage) -> None:
    # Use 'async with' context manager for processing the event
    async with event.process():
        # Decode the event body and store it as a string
        event_body = event.body.decode()

        # Log the decoded event
        logger.info(f"Got Events from charge point node (event={event_body})")
