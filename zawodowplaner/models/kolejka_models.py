from django.db import models

class Kolejka(models.Model):
    nazwa = models.CharField(max_length=50)
    data = models.DateTimeField()
    miejsce = models.CharField(max_length=100)
    zawody = models.ForeignKey('Zawody', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Kolejka"
        verbose_name_plural = "Kolejki"

    def __str__(self):
        return f"{self.nazwa} ({self.data})"