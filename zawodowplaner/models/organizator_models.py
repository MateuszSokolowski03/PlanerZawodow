from django.db import models

class Organizator(models.Model):
    id_organizatora = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefon = models.CharField(max_length=15, blank=True)
    data_utworzenia = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Organizator"
        verbose_name_plural = "Organizatorzy"

    def __str__(self):
        return self.nazwa