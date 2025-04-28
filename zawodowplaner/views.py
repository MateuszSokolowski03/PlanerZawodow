from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (
    zawody, kolejka, druzyna, zgloszenie,
    zawodnik, mecz, wydarzenie, powiadomienie, uzytkownik  # Dodaj uzytkownik
)


# Widok dla strony początkowej
class HomePageView(TemplateView):
    template_name = 'home.html'


# Widoki dla Zawodów
class ZawodyListView(ListView):
    model = zawody
    template_name = 'zawody/list.html'
    context_object_name = 'zawody'
    paginate_by = 10


class ZawodyDetailView(DetailView):
    model = zawody
    template_name = 'zawody/detail.html'


class ZawodyCreateView(LoginRequiredMixin, CreateView):
    model = zawody
    template_name = 'zawody/form.html'
    fields = ['nazwa', 'id_organizatora', 'data_rozpoczecia',
              'data_zakonczenia', 'opis', 'maks_zespolow', 'regulaminy']
    success_url = reverse_lazy('zawody-list')


class ZawodyUpdateView(LoginRequiredMixin, UpdateView):
    model = zawody
    template_name = 'zawody/form.html'
    fields = ['nazwa', 'data_rozpoczecia', 'data_zakonczenia',
              'opis', 'status', 'maks_zespolow', 'regulaminy']
    success_url = reverse_lazy('zawody-list')


class ZawodyDeleteView(LoginRequiredMixin, DeleteView):
    model = zawody
    template_name = 'zawody/confirm_delete.html'
    success_url = reverse_lazy('zawody-list')


# Widoki dla Kolejek
class KolejkaCreateView(LoginRequiredMixin, CreateView):
    model = kolejka
    template_name = 'kolejka/form.html'
    fields = ['id_zawodu', 'numer', 'nazwa', 'data_rozpoczecia', 'data_zakonczenia']
    success_url = reverse_lazy('zawody-list')


class KolejkaUpdateView(LoginRequiredMixin, UpdateView):
    model = kolejka
    template_name = 'kolejka/form.html'
    fields = ['numer', 'nazwa', 'data_rozpoczecia', 'data_zakonczenia', 'czy_zakonczona']
    success_url = reverse_lazy('zawody-list')


# Widoki dla Drużyn
class DruzynaListView(ListView):
    model = druzyna
    template_name = 'druzyna/list.html'
    context_object_name = 'druzyny'


class DruzynaCreateView(LoginRequiredMixin, CreateView):
    model = druzyna
    template_name = 'druzyna/form.html'
    fields = ['id_kapitana', 'nazwa', 'herb_url']
    success_url = reverse_lazy('druzyna-list')


# Widoki dla Zgłoszeń
class ZgloszenieCreateView(LoginRequiredMixin, CreateView):
    model = zgloszenie
    template_name = 'zgloszenie/form.html'
    fields = ['id_zawodu', 'id_druzyny']
    success_url = reverse_lazy('zgloszenie-list')

    def form_valid(self, form):
        form.instance.status = 'oczekujaca'
        return super().form_valid(form)


# Widoki dla Zawodników
class ZawodnikCreateView(LoginRequiredMixin, CreateView):
    model = zawodnik
    template_name = 'zawodnik/form.html'
    fields = ['id_druzyny', 'imie', 'nazwisko', 'data_urodzenia',
              'pozycja', 'numer_koszulki', 'zdjecie_url']
    success_url = reverse_lazy('druzyna-list')


# Widoki dla Meczy
class MeczDetailView(DetailView):
    model = mecz
    template_name = 'mecz/detail.html'


class MeczCreateView(LoginRequiredMixin, CreateView):
    model = mecz
    template_name = 'mecz/form.html'
    fields = ['id_kolejki', 'id_zawodu', 'data_meczu', 'miejsce',
              'druzyna_gospodarz', 'druzyna_gosc', 'sedzia_glowny']
    success_url = reverse_lazy('mecz-list')


# Widoki dla Powiadomień
class PowiadomienieListView(LoginRequiredMixin, ListView):
    model = powiadomienie
    template_name = 'powiadomienie/list.html'

    def get_queryset(self):
        # Pobierz instancję modelu `uzytkownik` powiązaną z aktualnym użytkownikiem
        try:
            uzytkownik_instance = uzytkownik.objects.get(email=self.request.user.email)
        except uzytkownik.DoesNotExist:
            return self.model.objects.none()

        # Filtruj powiadomienia dla tego użytkownika
        return self.model.objects.filter(id_uzytkownika=uzytkownik_instance)


class PowiadomienieUpdateView(LoginRequiredMixin, UpdateView):
    model = powiadomienie
    template_name = 'powiadomienie/form.html'
    fields = ['przeczytane']
    success_url = reverse_lazy('powiadomienie-list')