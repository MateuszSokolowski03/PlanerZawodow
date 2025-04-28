from django.contrib import admin
from django.urls import path
from zawodowplaner import views
from zawodowplaner.views import HomePageView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomePageView.as_view(), name='home'),

    path('zawody/', views.ZawodyListView.as_view(), name='zawody-list'),
    path('zawody/<int:pk>/', views.ZawodyDetailView.as_view(), name='zawody-detail'),
    path('zawody/dodaj/', views.ZawodyCreateView.as_view(), name='zawody-create'),
    path('zawody/<int:pk>/update/', views.ZawodyUpdateView.as_view(), name='zawody-update'),

    path('kolejka/dodaj/', views.KolejkaCreateView.as_view(), name='kolejka-create'),

    path('druzyny/', views.DruzynaListView.as_view(), name='druzyna-list'),

    path('powiadomienia/', views.PowiadomienieListView.as_view(), name='powiadomienie-list'),
]