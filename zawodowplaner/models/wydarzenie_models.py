from django.db import models

class Wydarzenie(models.Model):
    TYP_WYDARZENIA_WYBOR = [
        ('trening', 'Trening'),
        ('spotkanie', 'Spotkanie'),
        ('konferencja', 'Konferencja'),
        ('inne', 'Inne'),
    ]
    nazwa = models.CharField(max_length=100)
    data = models.DateTimeField()
    miejsce = models.CharField(max_length=100)
    typ = models.CharField(
        max_length=20,
        choices=TYP_WYDARZENIA_WYBOR,
        default='inne',
    )
    opis = models.TextField(blank=True)

    class Meta:
        verbose_name = "Wydarzenie"
        verbose_name_plural = "Wydarzenia"

    def __str__(self):
        return f"{self.nazwa} ({self.data})"