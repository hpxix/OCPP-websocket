from aio_pika.abc import AbstractIncomingMessage
from loguru import logger
import json
from charge_point_node.main import OnConnectionMessage, EventName
# from charge_point_node.main import OnconnectionEvent, EventName
import logging
from manager.services.charge_point import update_charge_point_status

logging.basicConfig(level=logging.INFO)


async def process_event(message: AbstractIncomingMessage) -> None:
    # Use 'async with' context manager for processing the event
    async with message.process():
        # Decode the message body and store it as a string and convert to json
        data = json.loads(message.body.decode())
        event_name = data["name"]
        # value because we have a value as a string and not an Enum object and map it to OnConnectionMessages
        event = {
            EventName.NEW_CONNECTION.value: OnConnectionMessage
        }[event_name](**data)
        # Log the decoded event
        logger.info(f"Got Events from charge point node (event={event})")

        # we need an Enum value because we need to compare objects with is operator and not comparison double equal ==
        if event.name is EventName.NEW_CONNECTION:
            status = "online"
            await update_charge_point_status(charge_point_id=event.charge_point_id, status=status)
