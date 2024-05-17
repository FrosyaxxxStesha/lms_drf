from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


@shared_task
def deactivate_users():
    User.objects.filter(last_login__lt=timezone.now() - timedelta(days=30)).update(is_active=False)
