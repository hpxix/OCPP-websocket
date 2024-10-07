# Import necessary libraries:
# - websockets: A WebSocket library for creating and managing WebSocket connections.
# - asyncio: A standard Python library to write concurrent code using async/await.
# - core.settings: A module (assumed to be in the user's project) that contains application configurations like WebSocket port.
# - loguru.logger: A third-party library for sophisticated logging with improved syntax and options over the built-in logging library.

import websockets
import asyncio
from core import settings
from loguru import logger
from websockets.legacy.server import WebSocketServerProtocol
import json
from core.settings import EVENT_QUEUE_NAME, TASK_QUEUE_NAME
from core.queue.publisher import publish
from core.queue.consumer import start_consume
from charge_point_node.services.tasks import process_task
from core.settings import WS_SERVER_PORT
from propan import Context, apply_types, Depends
from propan.annotations import ContextRepo
from propan.brokers.rabbit import RabbitQueue

import logging
logging.basicConfig(level=logging.DEBUG)


async def on_connect(connection: WebSocketServerProtocol, path: str):
    charge_point_id = path.strip("/")
    logger.info(
        f"New Charge Point Connected! (path={path}, charge_point_id={charge_point_id})")

    # Send a welcome message
    await connection.send("Welcome! You are now connected.")

    try:
        while True:
            # Wait for a message from the client
            message = await connection.recv()
            logger.info(f"Received message from {charge_point_id}: {message}")

            # Here, you can process the message if needed
            # For example, publish the message to the event queue
            await publish(message, to=EVENT_QUEUE_NAME)
            logging.info(f"Here is the EventQueueName:{EVENT_QUEUE_NAME}")
            # Optionally send a response back to the client
            await connection.send(f"Message received: {message}")

    except websockets.exceptions.ConnectionClosed:
        logger.info(f"Connection closed by the client: {charge_point_id}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        logger.info(f"Connection closed: {charge_point_id}")


async def main():

    asyncio.ensure_future(
        start_consume(TASK_QUEUE_NAME, on_message=process_task)
    )

    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        WS_SERVER_PORT,
    )
    logger.info(f"WebSocket server started at ws://0.0.0.0:{WS_SERVER_PORT}")
    await server.wait_closed()

if __name__ == "__main__":

    asyncio.run(main())
