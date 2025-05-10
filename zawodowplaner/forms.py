from django import forms
from django.contrib.auth.forms import UserCreationForm

from zawodowplaner.models import Organizator, Zawody, Kolejka, Wydarzenie, Uzytkownik


class OrganizatorForm(forms.ModelForm):
    class Meta:
        model = Organizator
        fields = ['nazwa', 'email', 'telefon']  # Dopasuj pola do modelu Organizator

class ZawodyForm(forms.ModelForm):
    class Meta:
        model = Zawody
        fields = ['nazwa', 'data_rozpoczecia', 'data_zakonczenia', 'status', 'opis']  # Dopasuj pola do modelu Zawody

class KolejkaForm(forms.ModelForm):
    class Meta:
        model = Kolejka
        fields = ['nazwa', 'data', 'miejsce', 'zawody']  # Dopasuj pola do modelu Kolejka

class WydarzenieForm(forms.ModelForm):
    class Meta:
        model = Wydarzenie
        fields = ['nazwa', 'data', 'miejsce', 'typ', 'opis']  # Dopasuj pola do modelu Wydarzenie


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adres e-mail")


class Meta:
    model = Uzytkownik
    fields = ['username', 'email', 'password1', 'password2']


def save(self, commit=True):
    user = super().save(commit=False)
    user.email = self.cleaned_data['email']
    if commit:
        user.save()
    return user