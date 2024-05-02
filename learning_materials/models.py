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
    """
    Модель курса. Является хранилищем для модели :model:`learning_materials.Lesson`.
    Содержит в себе ссылку на модель пользователя :model:`users.User`.
    """
    title = models.CharField(max_length=50,
                             verbose_name="название",
                             help_text="Название курса")
    preview = models.ImageField(upload_to="learning_materials/course/preview/",
                                default="learning_materials/course/preview/default/course.svg",
                                verbose_name="превью фото",
                                help_text="Фото, которое будет выбрано системой как превью-фото курса"
                                )
    description = models.TextField(verbose_name="описание",
                                   help_text="Описание курса")
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="course",
                             verbose_name="пользователь",
                             help_text="Пользователь, добавивший курс"
                             )

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    """
    Модель урока. Содержит в себе ссылки на курс :model:`learning_materials.Course`.
    Содержит в себе ссылку на модель пользователя :model:`users.User`.
    """
    title = models.CharField(max_length=50,
                             verbose_name="название",
                             help_text="Название курса"
                             )
    description = models.TextField(verbose_name="описание",
                                   help_text="Описание урока."
                                   )
    preview = models.ImageField(upload_to="learning_materials/lesson/preview/",
                                default="learning_materials/lesson/preview/default/lesson.svg",
                                verbose_name="Превью фото",
                                help_text="Фото-превью урока"
                                )
    video_link = models.URLField(verbose_name="ссылка на видео",
                                 **NULL,
                                 help_text="Видео курса. содержит основной контент")

    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name="lesson",
                               help_text="ссылка на модель курса"
                               )
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="lesson",
                             verbose_name="пользователь",
                             help_text="ссылка на модель пользователя"
                             )

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"


class Payment(models.Model):
    """
    Модель платежа за курс или урок.
    Ссылается на курс или урок:
    :model:`learning_materials.Course`
    :model:`learning_materials.Lesson`
    а также на пользователя, совершившего оплату:
    :model:`users.User`
    """
    payment_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name="дата оплаты",
                                        help_text="Дата оплаты за курс")
    amount = models.DecimalField(max_digits=16,
                                 decimal_places=8,
                                 verbose_name="сумма оплаты",
                                 help_text="Сумма оплаты за курс или урок"
                                 )
    method = models.CharField(max_length=4,
                              choices=PaymentMethodChoices,
                              verbose_name="способ оплаты",
                              help_text="Метод оплаты: CASH - наличные, TRNS - переводом на счёт"
                              )

    lesson = models.ForeignKey(Lesson,
                               on_delete=models.CASCADE,
                               **NULL,
                               verbose_name="оплаченный урок",
                               related_name="payment",
                               help_text="Ссылка на урок, по которому была произведена оплата. \
                               отсутствие означает, что оплата была произведена за курс"
                               )
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               **NULL,
                               verbose_name="оплаченный курс",
                               related_name="payment",
                               help_text="Ссылка на курс, по которому была произведена оплата. \
                               отсутствие означает, что оплата была произведена за урок"
                               )
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name="пользователь",
                             help_text="ссылка на модель пользователя"
                             )
