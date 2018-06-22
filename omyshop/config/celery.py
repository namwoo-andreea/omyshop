import os

from celery import Celery

os.environ.setdefault('DAJNGO_SETTINGS_MODULE', 'config.settings')

app = Celery('omyshop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()