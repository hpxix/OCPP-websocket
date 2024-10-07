import json
import logging
import asyncio

# Configure logging to track message processing and debugging
logging.basicConfig(level=logging.INFO)


async def process_task(message):
    """
    Processes incoming messages from the RabbitMQ queue.

    :param message: The incoming RabbitMQ message to be processed.
    :type message: aio_pika.IncomingMessage
    """
    try:
        # Decode the message body to a string
        message_body = message.body.decode("utf-8")

        # Convert the JSON string to a dictionary
        task_data = json.loads(message_body)

        # Log the received task for debugging
        logging.info(f"Received task: {task_data}")

        # Apply business logic here based on the message content
        # For example, if the message is a command to start charging:
        if task_data.get('command') == "start_charging":
            await handle_start_charging(task_data)
        elif task_data.get('command') == "stop_charging":  # Fixed typo in 'stop_charging'
            await handle_stop_charging(task_data)
        else:
            logging.warning(f"Unknown command received: {task_data.get('command')}")

        # Acknowledge the message after successful processing
        await message.ack()
        logging.info(f"Task Processed and Acknowledged: {task_data}")

    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode message: {e}")
        await message.nack(requeue=False)  # Fixed typo 'nackl' to 'nack'

    except Exception as e:
        logging.error(f"Error processing task: {e}")
        await message.nack(requeue=True)


async def handle_start_charging(task_data):
    """
    Example function for handling the start charging command.
    
    :param task_data: The task data containing command details.
    """
    # Implement the logic to start charging here
    logging.info(f"Starting a Charging Session: {task_data.get('session_id')}")

    # Simulate some async operation like interacting with a database or API
    await asyncio.sleep(1)
    logging.info(f"Charging Started for Session: {task_data.get('session_id')}")


async def handle_stop_charging(task_data):
    """
    Example function for handling the stop charging command.

    :param task_data: The task data containing command details.
    """
    # Implement the logic to stop charging here
    logging.info(f"Stopping Charging for Session: {task_data.get('session_id')}")

    # Simulate some async operation like interacting with a database or API
    await asyncio.sleep(1)
    logging.info(f"Charging Stopped for Session: {task_data.get('session_id')}")
