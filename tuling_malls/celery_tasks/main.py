import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tuling_malls.settings')
app=Celery('tuling')
app.config_from_object('celery_tasks.config')
app.autodiscover_tasks(['celery_tasks.sms'])