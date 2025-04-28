from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from zawodowplaner.models.liga_models import kolejka

class mecz(models.Model):
    TYP_STATUS_WYBOR = [
        ('planowany', 'planowany'),
        ('rozpoczety', 'rozpoczety'),
        ('zakonczony', 'zakonczony'),
    ]
        
    id_meczu = models.AutoField(primary_key=True)
    id_kolejki = models.ForeignKey('kolejka', on_delete=models.CASCADE)
    id_zawodu = models.ForeignKey('zawody', on_delete=models.CASCADE)
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

    def clean(self):
        # Sprawdź, czy drużyny są różne
        if self.druzyna_gospodarz == self.druzyna_gosc:
            raise ValidationError("Drużyny gospodarza i gościa muszą być różne.")
        
        if self.data_meczu < self.id_kolejki.data_rozpoczecia:
            raise ValidationError(f"Data meczu nie może być wcześniejsza niż data rozpoczęcia kolejki ({self.id_kolejki.data_rozpoczecia}).")
        
        if self.data_meczu > self.id_kolejki.data_zakonczenia:
            raise ValidationError(f"Data meczu nie może być późniejsza niż data zakończenia kolejki ({self.id_kolejki.data_zakonczenia}).")     
        
        # Sprawdź, czy mecz nie jest zaplanowany w tym samym czasie co inny mecz tej samej drużyny
        if mecz.objects.filter(
            models.Q(druzyna_gospodarz=self.druzyna_gospodarz) | 
            models.Q(druzyna_gosc=self.druzyna_gosc),
            data_meczu=self.data_meczu
        ).exclude(pk=self.pk).exists():
            raise ValidationError("Mecz tej drużyny już istnieje w tym czasie.")
        
        # Sprawdź, czy drużyny są z tego samego zawodu
        if self.druzyna_gospodarz.id_zawodu != self.druzyna_gosc.id_zawodu:
            raise ValidationError("Drużyny muszą być z tego samego zawodu.")
        
        # Sprawdź, czy dla meczu planowanego wyniki są zerowe
        if self.status == 'planowany' and (self.wynik_gospodarz != 0 or self.wynik_gosc != 0):
            raise ValidationError("Dla meczu planowanego wyniki muszą być 0-0.")
        
        # Sprawdź, czy wyniki nie są ujemne
        if self.wynik_gospodarz < 0 or self.wynik_gosc < 0:
            raise ValidationError("Wyniki nie mogą być ujemne.")

    class Meta:
        verbose_name = "Mecz"  
        verbose_name_plural = "Mecze"

    def __str__(self):
        return f"{self.druzyna_gospodarz} vs {self.druzyna_gosc} (Kolejka {self.id_kolejki.numer})"

@receiver(post_save, sender=mecz)
def zakonczenie_kolejki_po_meczu(sender, instance, **kwargs):
    """
    Automatycznie kończy kolejkę, jeśli wszystkie mecze w niej są zakończone.
    """
    kolejka_instance = instance.id_kolejki  # Pobierz kolejkę powiązaną z meczem
    if not kolejka_instance:
        return

    # Sprawdź, czy wszystkie mecze w kolejce mają status 'zakonczony'
    wszystkie_mecze_zakonczone = not kolejka_instance.mecz_set.filter(status__in=['planowany', 'rozpoczety']).exists()

    if wszystkie_mecze_zakonczone:
        kolejka_instance.czy_zakonczona = True
        kolejka_instance.save()



class wydarzenie(models.Model):
    TYP_ZDARZENIA_WYBOR = [
        ('bramka', 'Bramka'),
        ('kartka_zolta', 'Kartka Żółta'),
        ('kartka_czerwona', 'Kartka Czerwona'),
        ('zmiana', 'Zmiana'),
        ('rzut_karny', 'Rzut Karny'),
    ]
    id_wydarzenia = models.AutoField(primary_key=True)
    id_meczu = models.ForeignKey(mecz, on_delete=models.CASCADE)
    minuta = models.IntegerField(validators=[MinValueValidator(0)])
    typ = models.CharField(
        max_length=20,
        choices=TYP_ZDARZENIA_WYBOR,
    )
    id_zawodnika = models.ForeignKey('zawodnik', on_delete=models.CASCADE)
    id_druzyny = models.ForeignKey('druzyna', on_delete=models.CASCADE)
    komentarz = models.TextField(blank=True)

    def clean(self):
        # Sprawdź, czy mecz nie jest w statusie planowany
        if self.id_meczu.status == 'planowany':
            raise ValidationError("Nie można dodawać wydarzeń do meczu planowanego.")
        
        # Sprawdź, czy minuta nie jest ujemna
        if self.minuta < 0:
            raise ValidationError("Minuta nie może być ujemna.")
        
        # Sprawdź, czy zawodnik należy do odpowiedniej drużyny
        if self.id_zawodnika.id_druzyny != self.id_druzyny:
            raise ValidationError("Zawodnik musi należeć do wybranej drużyny.")
        
        # Walidacja bramek
        if self.typ == 'bramka':
            mecz = self.id_meczu
            if self.id_druzyny == mecz.druzyna_gospodarz.id_druzyny:
                # Sprawdź czy liczba bramek gospodarza nie przekracza wyniku
                bramki_gospodarza = wydarzenie.objects.filter(
                    id_meczu=mecz,
                    typ='bramka',
                    id_druzyny=mecz.druzyna_gospodarz.id_druzyny
                ).exclude(pk=self.pk).count()
                if bramki_gospodarza >= mecz.wynik_gospodarz:
                    raise ValidationError(f"Liczba bramek gospodarza nie może przekroczyć wyniku meczu ({mecz.wynik_gospodarz})")
            elif self.id_druzyny == mecz.druzyna_gosc.id_druzyny:
                # Sprawdź czy liczba bramek gości nie przekracza wyniku
                bramki_gosci = wydarzenie.objects.filter(
                    id_meczu=mecz,
                    typ='bramka',
                    id_druzyny=mecz.druzyna_gosc.id_druzyny
                ).exclude(pk=self.pk).count()
                if bramki_gosci >= mecz.wynik_gosc:
                    raise ValidationError(f"Liczba bramek gości nie może przekroczyć wyniku meczu ({mecz.wynik_gosc})")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Wydarzenie"  
        verbose_name_plural = "Wydarzenia"

    def __str__(self):
        return f"{self.typ} ({self.minuta} min) - {self.id_zawodnika} ({self.id_druzyny})"