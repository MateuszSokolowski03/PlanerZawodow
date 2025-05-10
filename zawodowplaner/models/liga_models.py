from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class Zawody(models.Model):
    TYP_STATUS_WYBOR = [
        ('oczekujaca', 'Oczekująca'),
        ('zatwierdzona', 'Zatwierdzona'),
        ('odrzucona', 'Odrzucona'),
        ('anulowane', 'Anulowane'),
    ]
    id_zawodu = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=50)
    id_organizatora = models.ForeignKey('Organizator', on_delete=models.CASCADE)
    data_rozpoczecia = models.DateTimeField()
    data_zakonczenia = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=TYP_STATUS_WYBOR,
        default='oczekujaca',
    )
    opis = models.TextField()
    czy_otwarta = models.BooleanField(default=False)
    maks_zespolow = models.IntegerField(validators=[MinValueValidator(1)])
    regulaminy = models.TextField()

    class Meta:
        verbose_name = "Zawody"
        verbose_name_plural = "Zawody"

    def __str__(self):
        return f"{self.nazwa} ({self.data_rozpoczecia} - {self.data_zakonczenia})"