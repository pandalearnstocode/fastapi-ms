import os
import time

from celery import Celery

# from cpu_load_generator import load_all_cores
from loguru import logger


def _short_task():
    logger.info("Short task")
    time.sleep(10)
    return {"task_duration": "Short task"}


def _medium_task():
    logger.info("Medium task")
    time.sleep(20)
    return {"task_duration": "Medium task"}


def _long_task():
    logger.info("Long task")
    time.sleep(30)
    return {"task_duration": "Long task"}


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)


@celery.task(name="create_task")
def create_task(task_type):
    if int(task_type) == 1:
        out = _short_task()
    elif int(task_type) == 2:
        out = _medium_task()
    elif int(task_type) == 3:
        out = _long_task()
    return out
