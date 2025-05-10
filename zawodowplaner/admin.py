from django.contrib import admin
from .models import (
    Uzytkownik,
    Powiadomienie,
    Mecz,
    Zawody,
    Druzyna,
    Kolejka,
    Wydarzenie,
    Zgloszenie,
    Organizator,
)

# Rejestracja modeli w panelu administracyjnym
@admin.register(Uzytkownik)
class UzytkownikAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'typ_uzytkownika', 'telefon')
    search_fields = ('email', 'username')
    list_filter = ('typ_uzytkownika',)

@admin.register(Powiadomienie)
class PowiadomienieAdmin(admin.ModelAdmin):
    list_display = ('tresc', 'data_wyslania', 'przeczytane', 'typ')
    list_filter = ('typ', 'przeczytane')
    search_fields = ('tresc',)

@admin.register(Mecz)
class MeczAdmin(admin.ModelAdmin):
    list_display = ('druzyna_gospodarz', 'druzyna_gosc', 'data_meczu', 'status', 'miejsce')
    list_filter = ('status', 'data_meczu')
    search_fields = ('druzyna_gospodarz__nazwa', 'druzyna_gosc__nazwa')

@admin.register(Zawody)
class ZawodyAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'data_rozpoczecia', 'data_zakonczenia', 'status', 'id_organizatora')
    list_filter = ('status', 'data_rozpoczecia')
    search_fields = ('nazwa', 'id_organizatora__nazwa')

@admin.register(Druzyna)
class DruzynaAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'data_utworzenia')
    search_fields = ('nazwa', 'data_utworzenia')

@admin.register(Kolejka)
class KolejkaAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'data', 'miejsce', 'zawody')
    list_filter = ('data',)
    search_fields = ('nazwa', 'zawody__nazwa')

@admin.register(Wydarzenie)
class WydarzenieAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'data', 'miejsce', 'typ')
    list_filter = ('typ', 'data')
    search_fields = ('nazwa',)

@admin.register(Zgloszenie)
class ZgloszenieAdmin(admin.ModelAdmin):
    list_display = ('druzyna', 'zawody', 'data_zgloszenia', 'status')
    list_filter = ('status', 'data_zgloszenia')
    search_fields = ('druzyna__nazwa', 'zawody__nazwa')

@admin.register(Organizator)
class OrganizatorAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'email', 'telefon', 'data_utworzenia')
    search_fields = ('nazwa', 'email')