from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Mecz(models.Model):
    TYP_STATUS_WYBOR = [
        ('planowany', 'Planowany'),
        ('rozpoczety', 'Rozpoczęty'),
        ('zakonczony', 'Zakończony'),
    ]
    id_meczu = models.AutoField(primary_key=True)
    id_kolejki = models.ForeignKey('Kolejka', on_delete=models.CASCADE)
    id_zawodu = models.ForeignKey('Zawody', on_delete=models.CASCADE)
    data_meczu = models.DateTimeField()
    druzyna_gospodarz = models.ForeignKey('Zgloszenie', related_name='gospodarze', on_delete=models.CASCADE)
    druzyna_gosc = models.ForeignKey('Zgloszenie', related_name='goscie', on_delete=models.CASCADE)
    wynik_gospodarz = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    wynik_gosc = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    status = models.CharField(
        max_length=20,
        choices=TYP_STATUS_WYBOR,
        default='planowany',
    )
    sedzia_glowny = models.CharField(max_length=50)
    miejsce = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Mecz"
        verbose_name_plural = "Mecze"

    def __str__(self):
        return f"{self.druzyna_gospodarz} vs {self.druzyna_gosc} (Kolejka {self.id_kolejki.numer})"