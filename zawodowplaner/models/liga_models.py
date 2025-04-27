from django.db import models
from django.core.validators import RegexValidator

from zawodowplaner.models import organizator


class liga(models.Model):
    id_ligi = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=50)
    poziom_rozgrywkowy = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    liczba_zespolow = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nazwa} ({self.poziom_rozgrywkowy})"
    

    
class zawody(models.Model):
    TYP_STATUS_WYBOR = [
        ('oczekujaca','oczekujaca'),
        ('zatwierdzona','zatwierdzona'),
        ('odrzucona','odrzucona'),
        ('anulowane', 'Anulowane'),
    ]

    id_zawodu = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=50)
    id_ligi = models.ForeignKey(liga,on_delete=models.CASCADE)
    id_organizatora = models.ForeignKey(organizator, on_delete=models.CASCADE)
    data_rozpoczecia = models.DateTimeField()
    data_zakonczenia = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=TYP_STATUS_WYBOR,
        default='planowane',
    )
    opis = models.TextField()
    czy_otwarta = models.BooleanField(default=False)
    maks_zespolow = models.IntegerField()
    regulaminy = models.TextField()

    def __str__(self):
        return f"{self.nazwa} ({self.data_rozpoczecia} - {self.data_zakonczenia})"
    

class kolejka(models.Model):
    id_kolejki = models.AutoField(primary_key=True)
    id_zawodu = models.ForeignKey(zawody, on_delete=models.CASCADE)
    numer = models.IntegerField()
    nazwa = models.CharField(max_length=100, blank=True)
    data_rozpoczecia = models.DateTimeField()
    data_zakonczenia = models.DateTimeField()
    czy_zakonczona = models.BooleanField(default=False)

    class Meta:
        unique_together = ('id_zawodu', 'numer')
        ordering = ['numer']

    def __str__(self):
        return f"Kolejka {self.numer} - {self.id_zawodu.nazwa}"

