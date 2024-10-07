# Core constant values of our app:
import os
from loguru import logger

# DEBUGGING
DEBUG = os.environ.get("DEBUG", "0") == "1"


# Using this pratice bellow ensures 3 key debugging features:
# 1-Strict and Explicit: It raises a KEYERROR immediately if the environment variable is not found, which is beneficial for required variables.
# 2-Error Detection: It helps detect missing configurations early, ensuring critical environment variables are set.
# 3-Clear Intent: Signals that the variable must be present for the application to run correctly.
WS_SERVER_PORT = int(os.environ["WS_SERVER_PORT"])
RABBIT_USER = os.environ["RABBIT_USER"]
RABBITMQ_DEFAULT_PASS = os.environ["RABBITMQ_DEFAULT_PASS"]
RABBITMQ_HOST = os.environ["RABBITMQ_HOST"]
RABBITMQ_PORT = int(os.environ["RABBITMQ_PORT"])
TASK_QUEUE_NAME = os.environ["TASK_QUEUE_NAME"]
EVENT_QUEUE_NAME = os.environ["EVENT_QUEUE_NAME"]

logger.add("csms.log", enqueue=True, backtrace=True,
           diagnose=DEBUG, format="{time} - {level} - {message}", rotation="10 MB", level="INFO")
