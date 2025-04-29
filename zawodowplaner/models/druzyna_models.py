from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class druzyna(models.Model):
    id_druzyny = models.AutoField(primary_key=True)
    id_kapitana = models.ForeignKey('kapitan', on_delete=models.CASCADE)
    nazwa = models.CharField(max_length=50)
    herb_url = models.URLField(max_length=200, blank=True)
    data_utworzenia = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Drużyna"  
        verbose_name_plural = "Drużyny"  
    
    def __str__(self):
        return self.nazwa

class zgloszenie(models.Model):
    TYP_STATUS_WYBOR = [
        ('oczekujaca','Oczekująca'),
        ('zatwierdzona','Zatwierdzona'),
        ('odrzucona','Odrzucona'),
    ]
    
    id_zgloszenia = models.AutoField(primary_key=True)
    id_zawodu = models.ForeignKey('zawody', on_delete=models.CASCADE)
    id_druzyny = models.ForeignKey(druzyna, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=TYP_STATUS_WYBOR,
        default='oczekujaca',
    )
    data_rejestracji = models.DateTimeField(auto_now_add=True)
    punkty = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    bramki_zdobyte = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    bramki_stracone = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ('id_zawodu', 'id_druzyny')
        verbose_name = "Zgłoszenie"  
        verbose_name_plural = "Zgłoszenia" 

    def clean(self):
        # Sprawdź, czy istnieje już zgłoszenie z tym samym kapitanem w tych samych zawodach
        if zgloszenie.objects.filter(
            id_zawodu=self.id_zawodu,
            id_druzyny__id_kapitana=self.id_druzyny.id_kapitana
        ).exclude(pk=self.pk).exists():
            raise ValidationError("Kapitan tej drużyny jest już zgłoszony w tych zawodach.")

    def __str__(self):
        return f"{self.id_druzyny.nazwa} - {self.id_zawodu.nazwa} ({self.status})"

class zawodnik(models.Model):
    TYP_POZYCJA_WYBOR = [
        ('bramkarz','Bramkarz'),
        ('obronca','Obrońca'),
        ('pomocnik','Pomocnik'),
        ('napastnik','Napastnik'),
    ]

    class Meta:
        verbose_name = "Zawodnik"  
        verbose_name_plural = "Zawodnicy"

    id_zawodnika = models.AutoField(primary_key=True)
    id_druzyny = models.ForeignKey('druzyna', on_delete=models.CASCADE)
    imie = models.CharField(max_length=50, validators=[RegexValidator(r'^[a-zA-Z]+$', 'Imię może zawierać tylko litery.')])
    nazwisko = models.CharField(max_length=50, validators=[RegexValidator(r'^[a-zA-Z]+$', 'Nazwisko może zawierać tylko litery.')])
    data_urodzenia = models.DateField()
    pozycja = models.CharField(
        max_length=50,
        choices=TYP_POZYCJA_WYBOR,
    )
    numer_koszulki = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    zdjecie_url = models.URLField(max_length=200, blank=True)

    def clean(self):
        super().clean()
        if self.data_urodzenia >= timezone.now().date():
            raise ValidationError("Data urodzenia musi być w przeszłości.")

    def __str__(self):
        return f"{self.imie} {self.nazwisko} ({self.pozycja})"
