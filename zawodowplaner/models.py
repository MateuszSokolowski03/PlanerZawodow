from django.db import models
from django.core.validators import RegexValidator

class uzytkownik(models.Model):
    TYP_UZYTKOWNIKA_WYBOR = [
        ('organizator', 'Organizator'),
        ('kapitan','Kapitan'),
        ('fan', 'Fan'),
    ]
    id_uzytkownika = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=254, unique=True)
    haslo_hash = models.CharField(max_length=128)
    typ_uzytkownika = models.CharField(
        max_length=20,
        choices=TYP_UZYTKOWNIKA_WYBOR,
        default='fan',
    )
    data_rejestracji = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} ({self.typ_uzytkownika})"




class organizator(models.Model):
    id_organizatora = models.AutoField(primary_key=True)
    id_uzytkownika = models.ForeignKey(uzytkownik, on_delete=models.CASCADE)
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    telefon = models.CharField(
        max_length = 9,
        validators=[RegexValidator(regex=r'^\d{9}$', message="Numer telefonu musi mieć 9 cyfr.")],
    )
    PESEL = models.CharField(
        max_length=11, 
        unique=True,
        validators=[RegexValidator(regex=r'^\d{11}$', message="PESEL musi mieć 11 cyfr.")],
    )
    data_dolaczenia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.imie} {self.nazwisko} ({self.telefon})"
    



class kapitan(models.Model):
    id_kapitana = models.AutoField(primary_key = True)
    id_uzytkownika = models.ForeignKey(uzytkownik, on_delete = models.CASCADE)
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    telefon = models.CharField(
        max_length = 9,
        validators=[RegexValidator(regex=r'^\d{9}$', message="Numer telefonu musi mieć 9 cyfr.")],
    )
    potwierdzony = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.imie} {self.nazwisko} ({self.telefon})"



class liga(models.Model):
    id_ligi = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=50)
    poziom_rozgrywkowy = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    liczba_zespolow = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nazwa} ({self.poziom_rozgrywkowy})"




class zawody(models.Model):
    TYP_STATUS_WYBOR = [
        ('oczekujaca','oczekujaca'),
        ('zatwierdzona','zatwierdzona'),
        ('odrzucona','odrzucona'),
        ('anulowane', 'Anulowane'),
    ]

    id_zawodu = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=50)
    id_ligi = models.ForeignKey(liga,on_delete=models.CASCADE)
    id_organizatora = models.ForeignKey(organizator, on_delete=models.CASCADE)
    data_rozpoczecia = models.DateTimeField()
    data_zakonczenia = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=TYP_STATUS_WYBOR,
        default='planowane',
    )
    opis = models.TextField()
    czy_otwarta = models.BooleanField(default=False)
    maks_zespolow = models.IntegerField()
    regulaminy = models.TextField()

    def __str__(self):
        return f"{self.nazwa} ({self.data_rozpoczecia} - {self.data_zakonczenia})"



class druzyna(models.Model):
    TYP_STATUS_WYBOR = [
        ('oczekujaca','oczekujaca'),
        ('zatwierdzona','zatwierdzona'),
        ('odrzucona','odrzucona'),
    ]
    id_druzyny = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=50)
    id_zawodu = models.ForeignKey(zawody, on_delete=models.CASCADE)
    id_kapitana = models.ForeignKey(kapitan, on_delete=models.CASCADE)
    herb_url = models.URLField(max_length=200, blank=True)
    data_rejestracji = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=TYP_STATUS_WYBOR,
        default='oczekujaca',
    )
    punkty = models.IntegerField(default=0)
    bramki_zdobyte = models.IntegerField(default=0)
    bramki_stracone = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nazwa} ({self.status})"



class zawodnik(models.Model):
    TYP_POZYCJA_WYBOR = [
        ('bramkarz','Bramkarz'),
        ('obronca','Obrońca'),
        ('pomocnik','Pomocnik'),
        ('napastnik','Napastnik'),
    ]
    id_zawodnika = models.AutoField(primary_key=True)
    id_druzyny = models.ForeignKey(druzyna, on_delete=models.CASCADE)
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    data_urodzenia = models.DateField()
    pozycja = models.CharField(
        max_length=50,
        choices=TYP_POZYCJA_WYBOR,
    )
    numer_koszulki = models.IntegerField()
    zdjecie_url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.imie} {self.nazwisko} ({self.pozycja})"



class mecz(models.Model):
    TYP_STATUS_WYBOR = [
        ('planowany','planowany'),
        ('rozpoczety','rozpoczety'),
        ('zakonczony','zakonczony'),
    ]
        
    id_meczu = models.AutoField(primary_key=True)
    id_zawodu = models.ForeignKey(zawody, on_delete=models.CASCADE)
    kolejka = models.IntegerField()
    data_meczu = models.DateTimeField()
    druzyna_gospodarz = models.ForeignKey(druzyna, related_name='druzyna_gospodarz', on_delete=models.CASCADE)
    druzyna_gosc = models.ForeignKey(druzyna, related_name='druzyna_gosc', on_delete=models.CASCADE)
    wynik_gospodarz = models.IntegerField(default=0)
    wynik_gosc = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=TYP_STATUS_WYBOR,
        default='planowany',
    )
    sedzia_glowny = models.CharField(max_length=50)
    miejsce = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.druzyna_gospodarz} vs {self.druzyna_gosc} ({self.data_meczu})"


class wydarzenie(models.Model):
    TYP_ZDARZENIA_WYBOR = [
        ('bramka','Bramka'),
        ('kartka_zolta','Kartka Żółta'),
        ('kartka_czerwona','Kartka Czerwona'),
        ('zmiana','Zmiana'),
        ('rzut_karny','Rzut Karny'),
    ]
    id_wydarzenia = models.AutoField(primary_key=True)
    id_meczu = models.ForeignKey(mecz, on_delete=models.CASCADE)
    minuta = models.IntegerField()
    typ = models.CharField(
        max_length=20,
        choices=TYP_ZDARZENIA_WYBOR,
    )
    id_zawodnika = models.ForeignKey(zawodnik, on_delete=models.CASCADE)
    id_druzyny = models.ForeignKey(druzyna, on_delete=models.CASCADE)
    komentarz = models.TextField(blank=True)

    def __str__(self):
        return f"{self.typ} ({self.minuta} min) - {self.id_zawodnika} ({self.id_druzyny})"



class powiadomienie(models.Model):
    TYP_POWIADOMIENIA_WYBOR = [
        ('systemowe','systemowe'),
        ('rejestracja','rejestracja'),
        ('mecz','mecz'),
    ]
    id_powiadomienia = models.AutoField(primary_key=True)
    id_uzytkownika = models.ForeignKey(uzytkownik, on_delete=models.CASCADE)
    tresc = models.TextField()
    data_wyslania= models.DateTimeField(auto_now_add=True)
    przeczytane = models.BooleanField(default=False)
    typ = models.CharField(
        max_length=20,
        choices=TYP_POWIADOMIENIA_WYBOR,
    )

    def __str__(self):
        return f"{self.tresc} ({self.data_wyslania})"