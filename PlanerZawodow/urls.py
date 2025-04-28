"""
URL configuration for PlanerZawodow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from zawodowplaner import views
from zawodowplaner.views import HomePageView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomePageView.as_view(), name='home'),

    # Organizatorzy
    path('organizatorzy/', views.OrganizatorListView.as_view(), name='organizator-list'),
    path('organizator/dodaj/', views.OrganizatorCreateView.as_view(), name='organizator-create'),

    # Kapitanowie
    path('kapitanowie/', views.KapitanListView.as_view(), name='kapitan-list'),
    path('kapitan/<int:pk>/', views.KapitanUpdateView.as_view(), name='kapitan-update'),

    # Użytkownicy
    path('uzytkownicy/', views.UzytkownikListView.as_view(), name='uzytkownik-list'),

    # Mecze
    path('mecz/', views.MeczListView.as_view(), name='mecz-list'),
    path('mecz/<int:pk>/', views.MeczUpdateView.as_view(), name='mecz-update'),

    # Wydarzenia
    path('wydarzenie/dodaj/', views.WydarzenieCreateView.as_view(), name='wydarzenie-create'),

    # Zawodnicy
    path('zawodnik/<int:pk>/', views.ZawodnikUpdateView.as_view(), name='zawodnik-update'),

    # Zawody
    path('zawody/', views.ZawodyListView.as_view(), name='zawody-list'),
    path('zawody/<int:pk>/', views.ZawodyDetailView.as_view(), name='zawody-detail'),
    path('zawody/dodaj/', views.ZawodyCreateView.as_view(), name='zawody-create'),

    # Kolejka
    path('kolejka/dodaj/', views.KolejkaCreateView.as_view(), name='kolejka-create'),

    # Drużyna
    path('druzyny/', views.DruzynaListView.as_view(), name='druzyna-list'),

    # Powiadomienia
    path('powiadomienia/', views.PowiadomienieListView.as_view(), name='powiadomienie-list'),
]
