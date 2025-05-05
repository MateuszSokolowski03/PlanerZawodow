from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _

class uzytkownik(AbstractUser):
    TYP_UZYTKOWNIKA_WYBOR = [
        ('organizator', 'Organizator'),
        ('kapitan', 'Kapitan'),
        ('fan', 'Fan'),
    ]
    
    username = None
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
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Użytkownik"
        verbose_name_plural = "Użytkownicy"

    def __str__(self):
        return self.email

class organizator(models.Model):
    user = models.OneToOneField(
        uzytkownik, 
        on_delete=models.CASCADE,
        related_name='organizator_profile'
    )
    imie = models.CharField(
        max_length=50,
        validators=[RegexValidator(regex=r'^[^\d]*$', message="Imię nie może zawierać cyfr.")],
    )
    nazwisko = models.CharField(
        max_length=50,
        validators=[RegexValidator(regex=r'^[^\d]*$', message="Nazwisko nie może zawierać cyfr.")],
    )
    PESEL = models.CharField(
        max_length=11, 
        unique=True,
        validators=[RegexValidator(regex=r'^\d{11}$', message="PESEL musi mieć 11 cyfr.")],
    )
    data_dolaczenia = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.user.typ_uzytkownika != 'organizator':
            raise ValidationError("Tylko użytkownik o typie 'organizator' może być przypisany jako organizator.")

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"

    class Meta:
        verbose_name = "Organizator"
        verbose_name_plural = "Organizatorzy"


class kapitan(models.Model):
    user = models.ForeignKey(
        uzytkownik,
        on_delete=models.CASCADE,
        related_name='kapitan_profiles'
    )
    potwierdzony = models.BooleanField(default=False)

    def clean(self):
        if self.user.typ_uzytkownika != 'kapitan':
            raise ValidationError("Tylko użytkownik o typie 'kapitan' może być przypisany jako kapitan.")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "Kapitan"
        verbose_name_plural = "Kapitanowie"