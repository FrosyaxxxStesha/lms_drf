from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Модель пользователя
    """
    username = None
    email = models.EmailField(
        verbose_name='почта',
        unique=True,
        help_text="Адресс электронной почты. Является логином, потому уникален"
    )
    phone_number = models.CharField(max_length=20,
                                    verbose_name="номер телефона",
                                    unique=True,
                                    null=True,
                                    blank=True,
                                    help_text="номер телефона пользователя. Уникален."
                                    ),
    city = models.CharField(max_length=50,
                            verbose_name="город",
                            help_text="Город проживания пользователя"
                            ),
    avatar = models.ImageField(upload_to="users/avatars",
                               default="users/avatars/default.svg",
                               verbose_name="аватар",
                               help_text="Аватар пользователя. Если пользователь не \
                                         заполняет это поле, то устанавливается стандартный аватар"
                               )

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        """
        Строковое значение, возвращающее поле, выбранное в качестве логина
        """
        return getattr(self, self.USERNAME_FIELD)
