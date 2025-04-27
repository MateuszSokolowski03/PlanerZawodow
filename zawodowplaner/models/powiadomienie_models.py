from django.db import models
from django.core.validators import RegexValidator

class powiadomienie(models.Model):
    TYP_POWIADOMIENIA_WYBOR = [
        ('systemowe','systemowe'),
        ('rejestracja','rejestracja'),
        ('mecz','mecz'),
    ]
    id_powiadomienia = models.AutoField(primary_key=True)
    id_uzytkownika = models.ForeignKey('uzytkownik', on_delete=models.CASCADE)
    tresc = models.TextField()
    data_wyslania= models.DateTimeField(auto_now_add=True)
    przeczytane = models.BooleanField(default=False)
    typ = models.CharField(
        max_length=20,
        choices=TYP_POWIADOMIENIA_WYBOR,
    )

    def __str__(self):
        return f"{self.tresc} ({self.data_wyslania})"