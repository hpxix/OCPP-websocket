from fastapi import FastAPI
import asyncio
from core.queue.consumer import start_consume
from core.settings import EVENT_QUEUE_NAME
from manager.controllers.status import status_router
from manager.services.event import process_event

import logging
logging.basicConfig(level=logging.DEBUG)


asyncio.ensure_future(
    start_consume(EVENT_QUEUE_NAME, on_message=process_event)
)

app = FastAPI()

app.include_router(status_router)
