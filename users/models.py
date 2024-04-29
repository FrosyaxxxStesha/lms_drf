from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name='почта',
        unique=True,
    )
    phone_number = models.CharField(max_length=20,
                                    verbose_name="номер телефона",
                                    unique=True,
                                    null=True,
                                    blank=True,
                                    ),
    city = models.CharField(max_length=50, verbose_name="город"),
    avatar = models.ImageField(upload_to="users/avatars", default="users/avatars/default.svg", verbose_name="аватар")

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return getattr(self, self.USERNAME_FIELD)
