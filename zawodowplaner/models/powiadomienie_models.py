from django.db import models

class Powiadomienie(models.Model):
    TYP_POWIADOMIENIA_WYBOR = [
        ('systemowe', 'Systemowe'),
        ('rejestracja', 'Rejestracja'),
        ('mecz', 'Mecz'),
    ]
    id_powiadomienia = models.AutoField(primary_key=True)
    id_uzytkownika = models.ForeignKey('Uzytkownik', on_delete=models.CASCADE)
    tresc = models.TextField()
    data_wyslania = models.DateTimeField(auto_now_add=True)
    przeczytane = models.BooleanField(default=False)
    typ = models.CharField(
        max_length=20,
        choices=TYP_POWIADOMIENIA_WYBOR,
    )

    class Meta:
        verbose_name = "Powiadomienie"
        verbose_name_plural = "Powiadomienia"

    def __str__(self):
        return f"{self.tresc} ({self.data_wyslania})"