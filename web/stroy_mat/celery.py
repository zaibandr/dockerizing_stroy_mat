from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stroy_mat.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Prod')

import configurations

configurations.setup()

app = Celery('stroy_mat')
# app.conf.broker_url = 'redis://:redis@{host}:{port}/0'.format(host=os.environ['REDIS_HOST'], port=6379)

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(
    broker_url='redis://:redis@{host}:{port}/0'.format(host=os.environ['REDIS_HOST'], port=6379),
    beat_scheduler='django_celery_beat.schedulers.DatabaseScheduler',
)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))