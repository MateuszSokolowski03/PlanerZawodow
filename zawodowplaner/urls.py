from django.urls import path
from zawodowplaner import views

urlpatterns = [
    # Strona główna
    path('', views.HomePageView.as_view(), name='user-main'),
    path('organizator/', views.OrganizatorMainPageView.as_view(), name='organizator-main'),

    # Organizatorzy
    path('organizatorzy/', views.OrganizatorListView.as_view(), name='organizator-list'),
    path('organizator/dodaj/', views.OrganizatorCreateView.as_view(), name='organizator-create'),

    # Użytkownicy
    path('uzytkownicy/', views.UzytkownikListView.as_view(), name='uzytkownik-list'),

    # Mecze
    path('mecze/', views.MeczListView.as_view(), name='mecz-list'),
    path('mecz/<int:pk>/', views.MeczUpdateView.as_view(), name='mecz-update'),

    # Wydarzenia
    path('wydarzenie/dodaj/', views.WydarzenieCreateView.as_view(), name='wydarzenie-create'),

    # Zawody
    path('zawody/', views.ZawodyListView.as_view(), name='zawody-list'),
    path('zawody/<int:pk>/', views.ZawodyDetailView.as_view(), name='zawody-detail'),
    path('zawody/dodaj/', views.ZawodyCreateView.as_view(), name='zawody-create'),
    path('zawody/<int:pk>/update/', views.ZawodyUpdateView.as_view(), name='zawody-update'),

    # Kolejki
    path('kolejka/dodaj/', views.KolejkaCreateView.as_view(), name='kolejka-create'),

    # Drużyny
    path('druzyny/', views.DruzynaListView.as_view(), name='druzyna-list'),

    # Powiadomienia
    path('powiadomienia/', views.PowiadomienieListView.as_view(), name='powiadomienie-list'),

    # Rejestracja
    path('register/', views.RegisterView.as_view(), name='register'),
]