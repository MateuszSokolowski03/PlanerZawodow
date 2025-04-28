from django.apps import AppConfig


class ZawodowplanerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'zawodowplaner'

def ready(self):
        import zawodowplaner.models.signals  # Rejestracja sygnałów