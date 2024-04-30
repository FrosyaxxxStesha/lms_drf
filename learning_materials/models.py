from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


NULL = {
    "null": True,
    "blank": True,
}


class PaymentMethodChoices(models.TextChoices):
    IN_CASH = "CASH", "payment in cash"
    TRANSFER = "TRNS",  "payment by transfer to the account"


class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name="название")
    preview = models.ImageField(upload_to="learning_materials/course/preview/",
                                default="learning_materials/course/preview/default/course.svg",
                                verbose_name="превью фото",
                                )
    description = models.TextField(verbose_name="описание")

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=50, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    preview = models.ImageField(upload_to="learning_materials/lesson/preview/",
                                default="learning_materials/lesson/preview/default/lesson.svg",
                                verbose_name="превью фото",
                                )
    video_link = models.URLField(verbose_name="ссылка на видео", **NULL)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lesson")

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"


class Payment(models.Model):
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="дата оплаты")
    amount = models.DecimalField(max_digits=16, decimal_places=8, verbose_name="сумма оплаты")
    method = models.CharField(max_length=4, choices=PaymentMethodChoices, verbose_name="способ оплаты")

    lesson = models.ForeignKey(Lesson,
                               on_delete=models.CASCADE,
                               **NULL,
                               verbose_name="оплаченный урок",
                               related_name="payment")
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               **NULL,
                               verbose_name="оплаченный курс",
                               related_name="payment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь")
