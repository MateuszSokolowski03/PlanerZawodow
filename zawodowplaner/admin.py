from django.contrib import admin
from django.utils.html import format_html
from .models import (
    uzytkownik, organizator, kapitan,
    zawody, kolejka,
    druzyna, zgloszenie, zawodnik,
    mecz, wydarzenie,
    powiadomienie
)


@admin.register(uzytkownik)
class UzytkownikAdmin(admin.ModelAdmin):
    list_display = ('email', 'typ_uzytkownika', 'data_rejestracji')
    list_filter = ('typ_uzytkownika', 'data_rejestracji')
    search_fields = ('email',)
    readonly_fields = ('data_rejestracji',)
    fieldsets = (
        ('Informacje podstawowe', {
            'fields': ('email', 'haslo_hash', 'typ_uzytkownika')
        }),
        ('Informacje dodatkowe', {
            'fields': ('data_rejestracji',)
        }),
    )


@admin.register(organizator)
class OrganizatorAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'imie', 'nazwisko', 'telefon', 'PESEL', 'data_dolaczenia')
    list_filter = ('data_dolaczenia',)
    search_fields = ('imie', 'nazwisko', 'telefon', 'PESEL', 'id_uzytkownika__email')
    readonly_fields = ('data_dolaczenia',)

    def get_email(self, obj):
        return obj.id_uzytkownika.email

    get_email.short_description = 'Email'
    get_email.admin_order_field = 'id_uzytkownika__email'


@admin.register(kapitan)
class KapitanAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'imie', 'nazwisko', 'telefon', 'potwierdzony')
    list_filter = ('potwierdzony',)
    search_fields = ('imie', 'nazwisko', 'telefon', 'id_uzytkownika__email')
    actions = ['potwierdz_kapitanow', 'odrzuc_kapitanow']

    def get_email(self, obj):
        return obj.id_uzytkownika.email

    get_email.short_description = 'Email'
    get_email.admin_order_field = 'id_uzytkownika__email'

    def potwierdz_kapitanow(self, request, queryset):
        queryset.update(potwierdzony=True)

    potwierdz_kapitanow.short_description = "Potwierdź wybranych kapitanów"

    def odrzuc_kapitanow(self, request, queryset):
        queryset.update(potwierdzony=False)

    odrzuc_kapitanow.short_description = "Odrzuć wybranych kapitanów"



@admin.register(zawody)
class ZawodyAdmin(admin.ModelAdmin):
    list_display = (
        'nazwa', 'get_organizator', 'data_rozpoczecia', 
        'data_zakonczenia', 'status', 'czy_otwarta'
    )
    list_filter = ('status', 'czy_otwarta')
    search_fields = ('nazwa', 'id_organizatora__imie', 'id_organizatora__nazwisko')
    readonly_fields = ('id_zawodu',)
    fieldsets = (
        ('Informacje podstawowe', {
            'fields': ('nazwa', 'id_organizatora', 'opis')
        }),
        ('Daty', {
            'fields': ('data_rozpoczecia', 'data_zakonczenia')
        }),
        ('Status i ustawienia', {
            'fields': ('status', 'czy_otwarta', 'maks_zespolow')
        }),
        ('Regulaminy', {
            'fields': ('regulaminy',),
            'classes': ('collapse',)
        }),
    )
    actions = ['zatwierdz_zawody', 'anuluj_zawody']

    def get_organizator(self, obj):
        return f"{obj.id_organizatora.imie} {obj.id_organizatora.nazwisko}"

    get_organizator.short_description = 'Organizator'
    get_organizator.admin_order_field = 'id_organizatora__nazwisko'

    def zatwierdz_zawody(self, request, queryset):
        queryset.update(status='zatwierdzona')

    zatwierdz_zawody.short_description = "Zatwierdź wybrane zawody"

    def anuluj_zawody(self, request, queryset):
        queryset.update(status='anulowane')

    anuluj_zawody.short_description = "Anuluj wybrane zawody"


@admin.register(kolejka)
class KolejkaAdmin(admin.ModelAdmin):
    list_display = ('id_zawodu', 'numer', 'nazwa', 'data_rozpoczecia', 'data_zakonczenia', 'czy_zakonczona')
    list_filter = ('czy_zakonczona', 'id_zawodu')
    search_fields = ('nazwa', 'id_zawodu__nazwa')
    actions = ['oznacz_jako_zakonczone', 'oznacz_jako_niezakonczone']

    def oznacz_jako_zakonczone(self, request, queryset):
        queryset.update(czy_zakonczona=True)

    oznacz_jako_zakonczone.short_description = "Oznacz wybrane kolejki jako zakończone"

    def oznacz_jako_niezakonczone(self, request, queryset):
        queryset.update(czy_zakonczona=False)

    oznacz_jako_niezakonczone.short_description = "Oznacz wybrane kolejki jako niezakończone"


@admin.register(druzyna)
class DruzynaAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'get_kapitan', 'data_utworzenia', 'get_liczba_zawodnikow')
    list_filter = ('data_utworzenia',)
    search_fields = ('nazwa', 'id_kapitana__imie', 'id_kapitana__nazwisko')
    readonly_fields = ('data_utworzenia',)
    
    def get_kapitan(self, obj):
        return f"{obj.id_kapitana.imie} {obj.id_kapitana.nazwisko}"
    
    get_kapitan.short_description = 'Kapitan'
    get_kapitan.admin_order_field = 'id_kapitana__nazwisko'
    
    def get_liczba_zawodnikow(self, obj):
        return obj.zawodnik_set.count()
    
    get_liczba_zawodnikow.short_description = 'Liczba zawodników'


@admin.register(zgloszenie)
class ZgloszenieAdmin(admin.ModelAdmin):
    list_display = ('get_druzyna', 'get_zawody', 'status', 'data_rejestracji', 'punkty', 'get_bilans_bramek')
    list_filter = ('status', 'id_zawodu')
    search_fields = ('id_druzyny__nazwa', 'id_zawodu__nazwa')
    readonly_fields = ('data_rejestracji',)
    actions = ['zatwierdz_zgloszenia', 'odrzuc_zgloszenia']
    
    def get_druzyna(self, obj):
        return obj.id_druzyny.nazwa
    
    get_druzyna.short_description = 'Drużyna'
    get_druzyna.admin_order_field = 'id_druzyny__nazwa'
    
    def get_zawody(self, obj):
        return obj.id_zawodu.nazwa
    
    get_zawody.short_description = 'Zawody'
    get_zawody.admin_order_field = 'id_zawodu__nazwa'
    
    def get_bilans_bramek(self, obj):
        return f"{obj.bramki_zdobyte}:{obj.bramki_stracone}"
    
    get_bilans_bramek.short_description = 'Bilans bramek'
    
    def zatwierdz_zgloszenia(self, request, queryset):
        queryset.update(status='zatwierdzona')
    
    zatwierdz_zgloszenia.short_description = "Zatwierdź wybrane zgłoszenia"
    
    def odrzuc_zgloszenia(self, request, queryset):
        queryset.update(status='odrzucona')
    
    odrzuc_zgloszenia.short_description = "Odrzuć wybrane zgłoszenia"


@admin.register(zawodnik)
class ZawodnikAdmin(admin.ModelAdmin):
    list_display = ('imie', 'nazwisko', 'get_druzyna', 'pozycja', 'numer_koszulki', 'data_urodzenia')
    list_filter = ('pozycja', 'id_druzyny')
    search_fields = ('imie', 'nazwisko', 'id_druzyny__nazwa')
    
    def get_druzyna(self, obj):
        return obj.id_druzyny.nazwa
    
    get_druzyna.short_description = 'Drużyna'
    get_druzyna.admin_order_field = 'id_druzyny__nazwa'
    
    def get_zdjecie(self, obj):
        if obj.zdjecie_url:
            return format_html(f'<img src="{obj.zdjecie_url}" width="50" height="50" />')
        return "-"
    
    get_zdjecie.short_description = 'Zdjęcie'


@admin.register(mecz)
class MeczAdmin(admin.ModelAdmin):
    list_display = ('get_mecz_info', 'id_zawodu', 'id_kolejki', 'data_meczu', 'status', 'get_wynik')
    list_filter = ('status', 'id_zawodu', 'id_kolejki')
    search_fields = (
        'druzyna_gospodarz__id_druzyny__nazwa', 
        'druzyna_gosc__id_druzyny__nazwa', 
        'miejsce'
    )
    readonly_fields = ('id_meczu',)
    fieldsets = (
        ('Informacje podstawowe', {
            'fields': ('id_zawodu', 'id_kolejki', 'data_meczu', 'miejsce')
        }),
        ('Drużyny', {
            'fields': ('druzyna_gospodarz', 'druzyna_gosc')
        }),
        ('Wynik', {
            'fields': ('wynik_gospodarz', 'wynik_gosc', 'status')
        }),
        ('Sędziowanie', {
            'fields': ('sedzia_glowny',)
        }),
    )
    actions = ['rozpocznij_mecze', 'zakoncz_mecze']
    
    def get_mecz_info(self, obj):
        return f"{obj.druzyna_gospodarz.id_druzyny} vs {obj.druzyna_gosc.id_druzyny}"
    
    get_mecz_info.short_description = 'Mecz'
    
    def get_wynik(self, obj):
        return f"{obj.wynik_gospodarz}:{obj.wynik_gosc}"
    
    get_wynik.short_description = 'Wynik'
    
    def rozpocznij_mecze(self, request, queryset):
        queryset.update(status='rozpoczety')
    
    rozpocznij_mecze.short_description = "Rozpocznij wybrane mecze"
    
    def zakoncz_mecze(self, request, queryset):
        queryset.update(status='zakonczony')
    
    zakoncz_mecze.short_description = "Zakończ wybrane mecze"


class WydarzenieInline(admin.TabularInline):
    model = wydarzenie
    extra = 1
    fields = ('minuta', 'typ', 'id_zawodnika', 'id_druzyny', 'komentarz')


@admin.register(wydarzenie)
class WydarzenieAdmin(admin.ModelAdmin):
    list_display = ('id_meczu', 'typ', 'minuta', 'id_zawodnika', 'get_druzyna')
    list_filter = ('typ', 'id_meczu')
    search_fields = ('id_zawodnika__imie', 'id_zawodnika__nazwisko', 'komentarz')
    
    def get_druzyna(self, obj):
        return obj.id_druzyny.nazwa
    
    get_druzyna.short_description = 'Drużyna'


@admin.register(powiadomienie)
class PowiadomienieAdmin(admin.ModelAdmin):
    list_display = ('get_uzytkownik', 'typ', 'data_wyslania', 'przeczytane')
    list_filter = ('typ', 'przeczytane', 'data_wyslania')
    search_fields = ('tresc', 'id_uzytkownika__email')
    readonly_fields = ('data_wyslania',)
    actions = ['oznacz_jako_przeczytane', 'oznacz_jako_nieprzeczytane']

    def get_uzytkownik(self, obj):
        return obj.id_uzytkownika.email

    get_uzytkownik.short_description = 'Użytkownik'
    get_uzytkownik.admin_order_field = 'id_uzytkownika__email'

    def oznacz_jako_przeczytane(self, request, queryset):
        queryset.update(przeczytane=True)

    oznacz_jako_przeczytane.short_description = "Oznacz wybrane powiadomienia jako przeczytane"

    def oznacz_jako_nieprzeczytane(self, request, queryset):
        queryset.update(przeczytane=False)

    oznacz_jako_nieprzeczytane.short_description = "Oznacz wybrane powiadomienia jako nieprzeczytane"


# Dodanie inline formularzy wydarzeń do meczu
MeczAdmin.inlines = [WydarzenieInline]