from celery import shared_task
from django.core.management import call_command

@shared_task
def calculate_daily_revenue():
    call_command('calculate_daily_revenue')