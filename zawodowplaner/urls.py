from django.urls import path, include
from zawodowplaner import views
from django.contrib.auth import views as auth_views
from .views import register, OrganizatorListView, register_partial
from .views import register_partial
from .views import CustomLoginView
from django.views.generic import TemplateView



urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('organizator/start/', TemplateView.as_view(template_name='organizator/start.html'), name='organizator-start'),
    path('register/partial/', register_partial, name='register_partial'),
    path('kapitan/start/', TemplateView.as_view(template_name='kapitan/start.html'), name='kapitan-start'),
    path('fan/start/', TemplateView.as_view(template_name='fan/start.html'), name='fan-start'),
]