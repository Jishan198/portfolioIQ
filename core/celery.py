import os
from celery import Celery

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
# Read config from settings.py with 'CELERY_' prefix
app.config_from_object('django.conf:settings', namespace='CELERY')
# Auto-discover tasks in all installed apps
app.autodiscover_tasks()