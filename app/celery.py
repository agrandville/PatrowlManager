# -*- coding: utf-8 -*-

import os
from celery import Celery
from django.conf import settings
from kombu import Exchange, Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# set the default Django settings module for the 'celery' program.
app = Celery('app', broker=settings.BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=10,
)

app.conf.broker_transport_options = {
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.2,
}

#app.conf.timezone = os.environ.get('PATROWL_TZ', 'Europe/Paris')

app.conf.task_queues = (
    # Default Queue / administrative purposes
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('scan', Exchange('scan'), routing_key='scan'),
)
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange = 'default'
app.conf.task_default_exchange_type = 'direct'
app.conf.task_default_routing_key = 'default'
