from django.db.models.signals import post_save
from django.dispatch import receiver
from zawodowplaner.models.liga_models import kolejka
from zawodowplaner.models.mecz_models import mecz

@receiver(post_save, sender=mecz)
def zakonczenie_kolejki_po_meczu(sender, instance, **kwargs):
    """
    Automatycznie kończy kolejkę, jeśli wszystkie mecze w niej są zakończone.
    """
    kolejka_instance = instance.id_kolejki  # Zakładam, że mecz ma pole `id_kolejki`
    if not kolejka_instance:
        return

    # Sprawdź, czy wszystkie mecze w kolejce są zakończone
    wszystkie_mecze_zakonczone = not kolejka_instance.mecz_set.filter(czy_zakonczony=False).exists()

    if wszystkie_mecze_zakonczone:
        kolejka_instance.czy_zakonczona = True
        kolejka_instance.save()