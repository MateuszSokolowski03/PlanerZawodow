from django.db import models
from django.core.validators import RegexValidator

class druzyna(models.Model):
    TYP_STATUS_WYBOR = [
        ('oczekujaca','oczekujaca'),
        ('zatwierdzona','zatwierdzona'),
        ('odrzucona','odrzucona'),
    ]
    id_druzyny = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=50)
    id_zawodu = models.ForeignKey('zawody', on_delete=models.CASCADE)
    id_kapitana = models.ForeignKey('kapitan', on_delete=models.CASCADE)
    herb_url = models.URLField(max_length=200, blank=True)
    data_rejestracji = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=TYP_STATUS_WYBOR,
        default='oczekujaca',
    )
    punkty = models.IntegerField(default=0)
    bramki_zdobyte = models.IntegerField(default=0)
    bramki_stracone = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nazwa} ({self.status})"

class zawodnik(models.Model):
    TYP_POZYCJA_WYBOR = [
        ('bramkarz','Bramkarz'),
        ('obronca','Obrońca'),
        ('pomocnik','Pomocnik'),
        ('napastnik','Napastnik'),
    ]
    id_zawodnika = models.AutoField(primary_key=True)
    id_druzyny = models.ForeignKey(druzyna, on_delete=models.CASCADE)
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    data_urodzenia = models.DateField()
    pozycja = models.CharField(
        max_length=50,
        choices=TYP_POZYCJA_WYBOR,
    )
    numer_koszulki = models.IntegerField()
    zdjecie_url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.imie} {self.nazwisko} ({self.pozycja})"