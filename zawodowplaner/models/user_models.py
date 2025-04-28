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
    class Meta:
        verbose_name = "Użytkownik"  
        verbose_name_plural = "Użytkownicy"
    

class organizator(models.Model):
    id_organizatora = models.AutoField(primary_key=True)
    id_uzytkownika = models.ForeignKey(uzytkownik, on_delete=models.CASCADE)
    imie = models.CharField(
        max_length=50,
        validators=[RegexValidator(regex=r'^[^\d]*$', message="Imię nie może zawierać cyfr.")],
    )
    nazwisko = models.CharField(
        max_length=50,
        validators=[RegexValidator(regex=r'^[^\d]*$', message="Nazwisko nie może zawierać cyfr.")],
    )
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
         # Sprawdź, czy istnieje już organizator z tym samym użytkownikiem
        if organizator.objects.filter(id_uzytkownika=self.id_uzytkownika).exists():
            raise ValidationError("Organizator z tym adresem e-mail już istnieje.")       

    def __str__(self):
        return f"{self.imie} {self.nazwisko} ({self.telefon})"
    class Meta:
        verbose_name = "Organizator"  
        verbose_name_plural = "Organizatorzy"
    

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
    class Meta:
        verbose_name = "Kapitan"  
        verbose_name_plural = "Kapitanowie"