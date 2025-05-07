from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import uzytkownik
from django.contrib.auth.models import BaseUserManager

class UzytkownikCreationForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=True, label="Nazwa użytkownika")

    class Meta:
        model = uzytkownik
        fields = ('username', 'email', 'first_name', 'last_name', 'telefon', 'typ_uzytkownika')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Usuwamy pomoc tekstową z pól hasła
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    # Dostosowanie pola email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if uzytkownik.objects.filter(email=email).exists():
            raise forms.ValidationError("Ten email jest już używany.")
        return email

class UzytkownikManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Email musi być podany')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

#    def create_superuser(self, email, username, password=None, **extra_fields):
#        extra_fields.setdefault('is_staff', True)
#        extra_fields.setdefault('is_superuser', True)

#        return self.create_user(email, username, password, **extra_fields)
    

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Usuwamy konieczność podania 'username', ponieważ używamy 'email'
        if 'username' in extra_fields:
            del extra_fields['username']

        return self.create_user(email, password, **extra_fields)
    

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
    username = forms.CharField(max_length=150, required=True, label="Nazwa użytkownika")

    class Meta:
        model = uzytkownik
        fields = ('username', 'email', 'password1', 'password2')

class KapitanRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=True, label="Nazwa użytkownika")

    class Meta:
        model = uzytkownik
        fields = ('username', 'email', 'first_name', 'last_name', 'telefon', 'password1', 'password2')

class OrganizatorRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=True, label="Nazwa użytkownika")
    PESEL = forms.CharField(max_length=11, required=True, label="PESEL")

    class Meta:
        model = uzytkownik
        fields = ('username', 'email', 'first_name', 'last_name', 'telefon', 'PESEL', 'password1', 'password2')

