from django.contrib.auth.views import LogoutView
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Organizator, Uzytkownik, Mecz, Wydarzenie, Zawody, Kolejka, Druzyna, Powiadomienie
from .forms import OrganizatorForm, ZawodyForm, KolejkaForm, WydarzenieForm, RegisterForm

# Strona główna
class HomePageView(LoginRequiredMixin, ListView):
    template_name = 'home.html'
    context_object_name = 'homepage'
    queryset = Zawody.objects.all()

class OrganizatorMainPageView(LoginRequiredMixin, ListView):
    template_name = 'zawodowplaner/zawody.html'
    context_object_name = 'mainpage'
    queryset = Zawody.objects.all()

# Organizatorzy
class OrganizatorListView(LoginRequiredMixin, ListView):
    model = Organizator
    template_name = 'zawodowplaner/organizatorzy.html'

class OrganizatorCreateView(LoginRequiredMixin, CreateView):
    model = Organizator
    form_class = OrganizatorForm
    template_name = 'zawodowplaner/organizator_form.html'
    success_url = reverse_lazy('organizator-list')

# Użytkownicy
class UzytkownikListView(LoginRequiredMixin, ListView):
    model = Uzytkownik
    template_name = 'zawodowplaner/uzytkownicy.html'

# Mecze
class MeczListView(LoginRequiredMixin, ListView):
    model = Mecz
    template_name = 'zawodowplaner/mecze.html'

class MeczUpdateView(LoginRequiredMixin, UpdateView):
    model = Mecz
    fields = ['druzyna_gospodarz', 'druzyna_gosc', 'wynik_gospodarz', 'wynik_gosc', 'data_meczu', 'miejsce', 'status']
    template_name = 'zawodowplaner/mecz_form.html'
    success_url = reverse_lazy('mecz-list')

# Wydarzenia
class WydarzenieCreateView(LoginRequiredMixin, CreateView):
    model = Wydarzenie
    form_class = WydarzenieForm
    template_name = 'zawodowplaner/wydarzenie_form.html'
    success_url = reverse_lazy('user-main')

# Zawodnicy
# class ZawodnikUpdateView(LoginRequiredMixin, UpdateView):
#     model = Zawodnik
#     fields = ['imie', 'nazwisko', 'druzyna']
#     template_name = 'zawodowplaner/zawodnik_form.html'
#     success_url = reverse_lazy('user-main')

# Zawody
class ZawodyListView(LoginRequiredMixin, ListView):
    model = Zawody
    template_name = 'zawodowplaner/zawody.html'

class ZawodyDetailView(LoginRequiredMixin, DetailView):
    model = Zawody
    template_name = 'zawodowplaner/zawody_detail.html'

class ZawodyCreateView(LoginRequiredMixin, CreateView):
    model = Zawody
    form_class = ZawodyForm
    template_name = 'zawodowplaner/zawody_form.html'
    success_url = reverse_lazy('zawody-list')

class ZawodyUpdateView(LoginRequiredMixin, UpdateView):
    model = Zawody
    form_class = ZawodyForm
    template_name = 'zawodowplaner/zawody_form.html'
    success_url = reverse_lazy('zawody-list')

# Kolejki
class KolejkaCreateView(LoginRequiredMixin, CreateView):
    model = Kolejka
    form_class = KolejkaForm
    template_name = 'zawodowplaner/kolejka_form.html'
    success_url = reverse_lazy('user-main')

# Drużyny
class DruzynaListView(LoginRequiredMixin, ListView):
    model = Druzyna
    template_name = 'zawodowplaner/druzyny.html'

# Powiadomienia
class PowiadomienieListView(LoginRequiredMixin, ListView):
    model = Powiadomienie
    template_name = 'zawodowplaner/powiadomienia.html'

# Rejestracja
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

# Wylogowanie
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')