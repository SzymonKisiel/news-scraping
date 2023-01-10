from time import sleep
from celery.utils.log import get_task_logger
from celery import Celery
from services.models import UpdateSentimentRequest
from services.sentiment_service import SentimentService
from database.env import is_docker

if is_docker():
    celery = Celery(
        'celery_app',
        # broker=config.CELERY_BROKER_URL,
        # backend=config.CELERY_RESULT_BACKEND
        backend='redis://redis:6379', broker='pyamqp://rabbitmq:5672'
    )
else:
    celery = Celery(
        'celery_app',
        # broker=config.CELERY_BROKER_URL,
        # backend=config.CELERY_RESULT_BACKEND
        backend='redis://localhost:6379', broker='pyamqp://localhost:5672'
    )

logger = get_task_logger(__name__)
sentiment_service = SentimentService(logger)


@celery.task()
def func1(arg: str):
    sleep(10)
    return 'Done: ' + arg


@celery.task()
def update_sentiments_task(search_term: str):
    sentiment_service.update(search_term)
    return f'Sentiments for {search_term} successfully updated'
