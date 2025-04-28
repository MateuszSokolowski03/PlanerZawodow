from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class uzytkownik(models.Model):
    TYP_UZYTKOWNIKA_WYBOR = [
        ('organizator', 'Organizator'),
        ('kapitan','Kapitan'),
        ('fan', 'Fan'),
    ]
    id_uzytkownika = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=254, unique=True)
    haslo_hash = models.CharField(max_length=128)
    typ_uzytkownika = models.CharField(
        max_length=20,
        choices=TYP_UZYTKOWNIKA_WYBOR,
        default='fan',
    )
    data_rejestracji = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} ({self.typ_uzytkownika})"
    

class organizator(models.Model):
    id_organizatora = models.AutoField(primary_key=True)
    id_uzytkownika = models.ForeignKey(uzytkownik, on_delete=models.CASCADE)
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    telefon = models.CharField(
        max_length = 9,
        validators=[RegexValidator(regex=r'^\d{9}$', message="Numer telefonu musi mieć 9 cyfr.")],
    )
    PESEL = models.CharField(
        max_length=11, 
        unique=True,
        validators=[RegexValidator(regex=r'^\d{11}$', message="PESEL musi mieć 11 cyfr.")],
    )
    data_dolaczenia = models.DateTimeField(auto_now_add=True)
    def clean(self):
        # Sprawdź, czy powiązany użytkownik ma typ "organizator"
        if self.id_uzytkownika.typ_uzytkownika != 'organizator':
            raise ValidationError("Tylko użytkownik o typie 'organizator' może być przypisany jako organizator.")
    def __str__(self):
        return f"{self.imie} {self.nazwisko} ({self.telefon})"
    

class kapitan(models.Model):
    id_kapitana = models.AutoField(primary_key = True)
    id_uzytkownika = models.ForeignKey(uzytkownik, on_delete = models.CASCADE)
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    telefon = models.CharField(
        max_length = 9,
        validators=[RegexValidator(regex=r'^\d{9}$', message="Numer telefonu musi mieć 9 cyfr.")],
    )
    potwierdzony = models.BooleanField(default=False)


    def clean(self):
        # Sprawdź, czy powiązany użytkownik ma typ "kapitan"
        if self.id_uzytkownika.typ_uzytkownika != 'kapitan':
            raise ValidationError("Tylko użytkownik o typie 'kapitan' może być przypisany jako kapitan.")
    def __str__(self):
        return f"{self.imie} {self.nazwisko} ({self.telefon})"
    
    def __str__(self):
        return f"{self.imie} {self.nazwisko} ({self.telefon})"