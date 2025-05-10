from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Druzyna(models.Model):
    id_druzyny = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=50)
    herb_url = models.URLField(max_length=200, blank=True)
    data_utworzenia = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Drużyna"
        verbose_name_plural = "Drużyny"

    def __str__(self):
        return self.nazwa