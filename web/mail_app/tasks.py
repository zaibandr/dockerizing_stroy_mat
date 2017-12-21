# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task
from .email import email_order_excel


@shared_task()
@periodic_task(run_every=crontab(minute="*/5"))
def send_order(email='panagoa@ya.ru'):
    email_order_excel(email)
