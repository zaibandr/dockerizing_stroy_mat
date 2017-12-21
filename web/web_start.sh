#!/usr/bin/env bash
/usr/local/bin/gunicorn --env DJANGO_SETTINGS_MODULE=stroy_mat.settings --env DJANGO_CONFIGURATION=Prod stroy_mat.wsgi:application -w 5 -t 120 -b :8000 --reload
flower -A stroy_mat --port=5555
celery -A stroy_mat worker -l info