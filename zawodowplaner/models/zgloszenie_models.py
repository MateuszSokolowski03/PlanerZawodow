from django.db import models

class Zgloszenie(models.Model):
    zawody = models.ForeignKey('Zawody', on_delete=models.CASCADE)
    druzyna = models.ForeignKey('Druzyna', on_delete=models.CASCADE)
    data_zgloszenia = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('nowe', 'Nowe'),
            ('zatwierdzone', 'Zatwierdzone'),
            ('odrzucone', 'Odrzucone'),
        ],
        default='nowe',
    )

    class Meta:
        verbose_name = "Zgłoszenie"
        verbose_name_plural = "Zgłoszenia"

    def __str__(self):
        return f"Zgłoszenie {self.druzyna} do {self.zawody}"