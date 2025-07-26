from celery import Celery
import os

def make_celery(app_name=__name__):
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    celery = Celery(
        app_name,
        broker=redis_url,
        backend=redis_url,
        include=['app.tasks']  # This tells Celery where to find tasks
    )

    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
    )

    return celery

celery = make_celery()
