# This will contain all our get_connection and get_channels functions, and also our singleton pattern design 
# to ensure that a class has only one instance, providing a global point of access to the instance. 
# This approach will help maintain consistency and save resources.

# Necessary packages:
from aio_pika import connect_robust
from aio_pika.abc import AbstractRobustChannel, AbstractRobustConnection
from loguru import logger
from core.settings import RABBIT_USER, RABBITMQ_DEFAULT_PASS, RABBITMQ_HOST, RABBITMQ_PORT, TASK_QUEUE_NAME, EVENT_QUEUE_NAME

# Singleton Pattern Design
_connection: AbstractRobustConnection | None = None
_tasks_channel: AbstractRobustChannel | None = None
_event_channel: AbstractRobustChannel | None = None

# Get_connection verifies if the connection object exists; 
# if it doesn't, it creates a new one and returns it.
async def get_connection() -> AbstractRobustConnection:
    
    global _connection
    if not _connection:
        _connection = await connect_robust(
            f"amqp://{RABBIT_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"
        )
        logger.info(
            f"Got Queue Connection (user={RABBIT_USER}, host={RABBITMQ_HOST}, port={RABBITMQ_PORT})"
        )
    return _connection

# get_channel checks if the channel object exists; if not, it creates a new channel.
async def get_channel(connection: AbstractRobustConnection, queue: str) -> AbstractRobustChannel:
    global _tasks_channel, _event_channel  # Declare all global variables at once
    if queue == TASK_QUEUE_NAME:
        if not _tasks_channel:
            _tasks_channel = await connection.channel()
        return _tasks_channel
    elif queue == EVENT_QUEUE_NAME:
        if not _event_channel:
            _event_channel = await connection.channel()
        return _event_channel
