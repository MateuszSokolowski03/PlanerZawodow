from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.timezone import now

from zawodowplaner.models import organizator


    
class zawody(models.Model):
    TYP_STATUS_WYBOR = [
        ('oczekujaca','oczekujaca'),
        ('zatwierdzona','zatwierdzona'),
        ('odrzucona','odrzucona'),
        ('anulowane', 'Anulowane'),
    ]

    id_zawodu = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=50)
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
    class Meta:
        verbose_name = "Zawody"  
        verbose_name_plural = "Zawody"

    def clean(self):
        if self.data_rozpoczecia >= self.data_zakonczenia:
            raise ValidationError("Data rozpoczęcia musi być wcześniejsza niż data zakończenia.")


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
        verbose_name = "Kolejka"  
        verbose_name_plural = "Kolejki"

    def __str__(self):
        return f"Kolejka {self.numer} - {self.id_zawodu.nazwa}"

