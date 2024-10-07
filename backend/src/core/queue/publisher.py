
# import nesscary packages

import aio_pika

# import get_connection and get_channel from core -> __init__.py

from core.queue import get_connection, get_channel

# in our publisher we get connection and we get channel and we publish our message in byte representation


async def publish(data: str, to: str) -> None:
    connection = await get_connection()
    channel = await get_channel(connection, to)

    await channel.default_exchange.publish(
        aio_pika.Message(
            bytes(data, "utf-8"),
            content_type="json",
        ),
        routing_key=to,
    )
