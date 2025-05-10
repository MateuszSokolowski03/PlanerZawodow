from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


class Uzytkownik(AbstractUser):
    TYP_UZYTKOWNIKA_WYBOR = [
        ('organizator', 'Organizator'),
        ('fan', 'Fan'),
    ]

    username = models.CharField(max_length=150, unique=True, default="default_user")
    email = models.EmailField('email address', unique=True)
    typ_uzytkownika = models.CharField(
        max_length=20,
        choices=TYP_UZYTKOWNIKA_WYBOR,
        default='fan',
    )
    telefon = models.CharField(
        max_length=9,
        validators=[RegexValidator(regex=r'^\d{9}$', message="Numer telefonu musi mieć 9 cyfr.")],
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Użytkownik"
        verbose_name_plural = "Użytkownicy"

    def __str__(self):
        return self.email