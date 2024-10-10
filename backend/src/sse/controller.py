from fastapi import APIRouter
from starlette.requests import Request
from sse_starlette.sse import EventSourceResponse
import asyncio
from typing import List
from charge_point_node.main import BaseEvent

stream_router = APIRouter(tags=["stream"])


class Publisher:
    def __init__(self):
        # Initialize the observers list
        self.observers: List["Observer"] = []

    async def add_observer(self, observer: "Observer") -> None:
        self.observers.append(observer)

    async def remove_observer(self, observer: "Observer") -> None:
        self.observers.remove(observer)

    async def publish(self, event: BaseEvent) -> None:
        for observer in self.observers:
            await observer.put(event)


class Observer(asyncio.Queue):

    async def subscribe(self, publisher: Publisher):
        await publisher.add_observer(self)

    async def unsubscribe(self, publisher: Publisher):
        await publisher.remove_observer(self)


async def event_generator():
    while True:
        yield "works"
        await asyncio.sleep(0.5)


@stream_router.get("/stream")
async def stream(request: Request):
    return EventSourceResponse(event_generator())
