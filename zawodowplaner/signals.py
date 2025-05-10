from django.db.models.signals import post_save
from django.dispatch import receiver
from zawodowplaner.models.kolejka_models import Kolejka
from zawodowplaner.models.mecz_models import Mecz
from zawodowplaner.models.zgloszenie_models import Zgloszenie

@receiver(post_save, sender=Mecz)
def zakonczenie_kolejki_po_meczu(sender, instance, created, **kwargs):
    """
    Automatycznie kończy kolejkę, jeśli wszystkie mecze w niej są zakończone.
    Aktualizuje bilans i liczbę punktów drużyn po zakończeniu meczu.
    """
    # Aktualizacja bilansu i punktów drużyn tylko jeśli mecz został zmieniony na 'zakonczony'
    if instance.status == 'zakonczony' and not created:
        zgloszenie_gospodarz = instance.druzyna_gospodarz
        zgloszenie_gosc = instance.druzyna_gosc

        # Aktualizacja punktów i bilansu
        if instance.wynik_gospodarz > instance.wynik_gosc:
            zgloszenie_gospodarz.punkty += 3
        elif instance.wynik_gospodarz < instance.wynik_gosc:
            zgloszenie_gosc.punkty += 3
        else:
            zgloszenie_gospodarz.punkty += 1
            zgloszenie_gosc.punkty += 1

        # Aktualizacja bramek
        zgloszenie_gospodarz.bramki_zdobyte += instance.wynik_gospodarz
        zgloszenie_gospodarz.bramki_stracone += instance.wynik_gosc
        zgloszenie_gosc.bramki_zdobyte += instance.wynik_gosc
        zgloszenie_gosc.bramki_stracone += instance.wynik_gospodarz

        zgloszenie_gospodarz.save()
        zgloszenie_gosc.save()

    # Sprawdź, czy wszystkie mecze w kolejce są zakończone
    kolejka_instance = instance.id_kolejki
    if not kolejka_instance:
        return

    wszystkie_mecze_zakonczone = not kolejka_instance.mecz_set.filter(status__in=['planowany', 'rozpoczety']).exists()

    if wszystkie_mecze_zakonczone:
        kolejka_instance.czy_zakonczona = True
        kolejka_instance.save()