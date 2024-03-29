from celery import Celery
from celery.schedules import crontab

app = Celery('yourapp')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'calculate_daily_revenue': {
        'task': 'yourapp.tasks.calculate_daily_revenue',
        'schedule': crontab(hour=0, minute=0),  
    },
}

