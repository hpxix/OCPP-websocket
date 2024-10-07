# Import nescary packages: asyncio

import asyncio

# import get_connection and get_channel from core.queue

from core.queue import get_connection, get_channel

#This is the function for consuming messages from the queue no matter what is it tasks, events etc...
async def start_consume(
    queue_name,
    on_message,
    prefetch_count=100,
    durable=True
) -> None:

    connection = await get_connection()
    channel = await get_channel(connection, queue_name)

    await channel.set_qos(prefetch_count=prefetch_count)
    queue = await channel.declare_queue(queue_name, durable=durable)

    await queue.consume(on_message)

    try:
        await asyncio.Future()

    finally:
        await connection.close()
