from django.urls import path, include
from zawodowplaner import views
from django.contrib.auth import views as auth_views
from .views import register, OrganizatorListView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('organizator/list/', OrganizatorListView.as_view(), name='organizator-list'),
]