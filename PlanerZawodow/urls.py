from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from zawodowplaner import views
from zawodowplaner.views import CustomLogoutView

urlpatterns = [
    # Panel administracyjny
    path('admin/', admin.site.urls),

    # Strona główna
    path('', views.HomePageView.as_view(), name='user-main'),
    path('organizator/', include('zawodowplaner.urls'), name='organizator-main'),  # Przekierowanie do aplikacji zawodowplaner

    # Rejestracja i logowanie
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]