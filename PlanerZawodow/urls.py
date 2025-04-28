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

    path('zawody/', views.ZawodyListView.as_view(), name='zawody-list'),
    path('zawody/<int:pk>/', views.ZawodyDetailView.as_view(), name='zawody-detail'),
    path('zawody/dodaj/', views.ZawodyCreateView.as_view(), name='zawody-create'),

    path('kolejka/dodaj/', views.KolejkaCreateView.as_view(), name='kolejka-create'),

    path('druzyny/', views.DruzynaListView.as_view(), name='druzyna-list'),

    path('powiadomienia/', views.PowiadomienieListView.as_view(), name='powiadomienie-list'),
]
