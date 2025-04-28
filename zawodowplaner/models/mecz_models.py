from django.db import models
from django.core.validators import RegexValidator

class mecz(models.Model):
    TYP_STATUS_WYBOR = [
        ('planowany','planowany'),
        ('rozpoczety','rozpoczety'),
        ('zakonczony','zakonczony'),
    ]
        
    id_meczu = models.AutoField(primary_key=True)
    id_kolejki = models.ForeignKey('kolejka', on_delete=models.CASCADE)
    id_zawodu = models.ForeignKey('zawody', on_delete=models.CASCADE)
    data_meczu = models.DateTimeField()
    druzyna_gospodarz = models.ForeignKey('Zgloszenie', related_name='gospodarze', on_delete=models.CASCADE)
    druzyna_gosc = models.ForeignKey('Zgloszenie', related_name='goscie', on_delete=models.CASCADE)
    wynik_gospodarz = models.IntegerField(default=0)
    wynik_gosc = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=TYP_STATUS_WYBOR,
        default='planowany',
    )
    sedzia_glowny = models.CharField(max_length=50)
    miejsce = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.druzyna_gospodarz} vs {self.druzyna_gosc} (Kolejka {self.id_kolejki.numer})"

    class Meta:
        verbose_name = "Mecz"  
        verbose_name_plural = "Mecze"

class wydarzenie(models.Model):
    TYP_ZDARZENIA_WYBOR = [
        ('bramka','Bramka'),
        ('kartka_zolta','Kartka Żółta'),
        ('kartka_czerwona','Kartka Czerwona'),
        ('zmiana','Zmiana'),
        ('rzut_karny','Rzut Karny'),
    ]
    id_wydarzenia = models.AutoField(primary_key=True)
    id_meczu = models.ForeignKey(mecz, on_delete=models.CASCADE)
    minuta = models.IntegerField()
    typ = models.CharField(
        max_length=20,
        choices=TYP_ZDARZENIA_WYBOR,
    )
    id_zawodnika = models.ForeignKey('zawodnik', on_delete=models.CASCADE)
    id_druzyny = models.ForeignKey('druzyna', on_delete=models.CASCADE)
    komentarz = models.TextField(blank=True)

    def __str__(self):
        return f"{self.typ} ({self.minuta} min) - {self.id_zawodnika} ({self.id_druzyny})"
    
    class Meta:
        verbose_name = "Wydarzenie"  
        verbose_name_plural = "Wydarzenia"