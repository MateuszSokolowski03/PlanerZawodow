from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import uzytkownik

class UzytkownikCreationForm(UserCreationForm):
    class Meta:
        model = uzytkownik
        fields = ('email', 'first_name', 'last_name', 'telefon', 'typ_uzytkownika')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

class UzytkownikChangeForm(UserChangeForm):
    class Meta:
        model = uzytkownik
        fields = ('email', 'first_name', 'last_name', 'telefon', 'typ_uzytkownika', 'is_active', 'is_staff', 'is_superuser')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].help_text = "Hasła nie przechowujemy w postaci tekstowej, więc nie można zobaczyć hasła tego użytkownika."

class RegistrationForm(UzytkownikCreationForm):
    class Meta(UzytkownikCreationForm.Meta):
        fields = UzytkownikCreationForm.Meta.fields

class FanRegistrationForm(UserCreationForm):
    class Meta:
        model = uzytkownik
        fields = ('email', 'password1', 'password2')

class KapitanRegistrationForm(UserCreationForm):
    class Meta:
        model = uzytkownik
        fields = ('email', 'first_name', 'last_name', 'telefon', 'password1', 'password2')

class OrganizatorRegistrationForm(UserCreationForm):
    PESEL = forms.CharField(max_length=11, required=True, label="PESEL")

    class Meta:
        model = uzytkownik
        fields = ('email', 'first_name', 'last_name', 'telefon', 'PESEL', 'password1', 'password2')
