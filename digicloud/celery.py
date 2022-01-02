import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digicloud.settings')

app = Celery('digicloud', broker=settings.CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'update all sendinblue users': {
        'task': 'digicloud.fetcher.tasks.update_all_rss',
        'schedule': crontab(minute=30),
        'options': {'queue': 'rss_update'}  # noqa F405
    }
}
