import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'subscription_system.settings')

app = Celery('subscription_system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'fetch-usd-to-bdt-hourly': {
        'task': 'subscriptions.tasks.fetch_usd_to_bdt_exchange_rate',
        'schedule': crontab(hour='*', minute=0),  
    },
}