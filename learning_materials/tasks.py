from celery import shared_task
from django.core.mail import send_mail

from learning_materials import models


@shared_task
def course_updated_notification(id):
    course = models.Course.objects.get(id=id)
    subject = "Обновление курса"
    message = f'Курс "{course.title}" обновлён'
    users_email = [subscription.user.email for subscription in course.subscription.all().prefetch_related("user")]
    send_mail(subject, message, None, users_email)
