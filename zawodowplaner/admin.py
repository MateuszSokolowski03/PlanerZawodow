from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin
from .models import (
    uzytkownik, organizator, kapitan,
    zawody, kolejka,
    druzyna, zgloszenie, zawodnik,
    mecz, wydarzenie,
    powiadomienie
)
from .forms import UzytkownikCreationForm, UzytkownikChangeForm


@admin.register(uzytkownik)
class UzytkownikAdmin(UserAdmin):
    add_form = UzytkownikCreationForm
    form = UzytkownikChangeForm
    list_display = ('email', 'first_name', 'last_name', 'typ_uzytkownika', 'telefon', 'is_staff')
    list_filter = ('typ_uzytkownika', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name', 'telefon')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Dane osobowe', {'fields': ('first_name', 'last_name', 'telefon')}),
        ('Uprawnienia', {
            'fields': ('typ_uzytkownika', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Ważne daty', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'telefon', 'typ_uzytkownika'),
        }),
    )

@admin.register(organizator)
class OrganizatorAdmin(admin.ModelAdmin):
    list_display = ('user', 'imie', 'nazwisko', 'PESEL', 'data_dolaczenia')
    list_filter = ('data_dolaczenia',)
    search_fields = ('imie', 'nazwisko', 'PESEL', 'user__email', 'user__telefon')
    readonly_fields = ('data_dolaczenia', 'user')
    fieldsets = (
        (None, {
            'fields': ('user', 'imie', 'nazwisko', 'PESEL')
        }),
        ('Dane dodatkowe', {
            'fields': ('data_dolaczenia',)
        }),
    )

@admin.register(kapitan)
class KapitanAdmin(admin.ModelAdmin):
    list_display = ('user', 'potwierdzony', 'get_telefon')
    list_filter = ('potwierdzony',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'user__telefon')
    readonly_fields = ('user',)
    actions = ['potwierdz_kapitanow', 'odrzuc_kapitanow']

    def get_telefon(self, obj):
        return obj.user.telefon
    get_telefon.short_description = 'Telefon'

    def potwierdz_kapitanow(self, request, queryset):
        updated = queryset.update(potwierdzony=True)
        self.message_user(request, f"Potwierdzono {updated} kapitanów")
    potwierdz_kapitanow.short_description = "Potwierdź wybranych kapitanów"

    def odrzuc_kapitanow(self, request, queryset):
        updated = queryset.update(potwierdzony=False)
        self.message_user(request, f"Odrzucono {updated} kapitanów")
    odrzuc_kapitanow.short_description = "Odrzuć wybranych kapitanów"

@admin.register(zawody)
class ZawodyAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'id_organizatora', 'data_rozpoczecia', 'data_zakonczenia', 'status', 'czy_otwarta')
    list_filter = ('status', 'czy_otwarta', 'data_rozpoczecia')
    search_fields = ('nazwa', 'id_organizatora__user__email', 'id_organizatora__imie', 'id_organizatora__nazwisko')
    readonly_fields = ()
    fieldsets = (
        ('Informacje podstawowe', {
            'fields': ('nazwa', 'id_organizatora', 'opis')
        }),
        ('Terminy', {
            'fields': ('data_rozpoczecia', 'data_zakonczenia')
        }),
        ('Ustawienia', {
            'fields': ('status', 'czy_otwarta', 'maks_zespolow')
        }),
        ('Regulamin', {
            'fields': ('regulaminy',),
            'classes': ('collapse',)
        }),
    )
    actions = ['zatwierdz_zawody', 'anuluj_zawody']

    def zatwierdz_zawody(self, request, queryset):
        updated = queryset.update(status='zatwierdzona')
        self.message_user(request, f"Zatwierdzono {updated} zawodów")
    zatwierdz_zawody.short_description = "Zatwierdź wybrane zawody"

    def anuluj_zawody(self, request, queryset):
        updated = queryset.update(status='anulowane')
        self.message_user(request, f"Anulowano {updated} zawodów")
    anuluj_zawody.short_description = "Anuluj wybrane zawody"

@admin.register(kolejka)
class KolejkaAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'id_zawodu', 'numer', 'data_rozpoczecia', 'data_zakonczenia', 'czy_zakonczona')
    list_filter = ('czy_zakonczona', 'id_zawodu')
    search_fields = ('nazwa', 'id_zawodu__nazwa')
    date_hierarchy = 'data_rozpoczecia'
    actions = ['oznacz_jako_zakonczone', 'oznacz_jako_niezakonczone']

    def oznacz_jako_zakonczone(self, request, queryset):
        updated = queryset.update(czy_zakonczona=True)
        self.message_user(request, f"Oznaczono {updated} kolejek jako zakończone")
    oznacz_jako_zakonczone.short_description = "Oznacz jako zakończone"

    def oznacz_jako_niezakonczone(self, request, queryset):
        updated = queryset.update(czy_zakonczona=False)
        self.message_user(request, f"Oznaczono {updated} kolejek jako niezakończone")
    oznacz_jako_niezakonczone.short_description = "Oznacz jako niezakończone"

@admin.register(druzyna)
class DruzynaAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'id_kapitana', 'data_utworzenia')
    list_filter = ('data_utworzenia',)
    search_fields = ('nazwa', 'id_kapitana__user__email')
    readonly_fields = ('data_utworzenia',)

@admin.register(zgloszenie)
class ZgloszenieAdmin(admin.ModelAdmin):
    list_display = ('id_druzyny', 'id_zawodu', 'status', 'data_rejestracji', 'punkty', 'bilans_bramek')
    list_filter = ('status', 'id_zawodu')
    search_fields = ('id_druzyny__nazwa', 'id_zawodu__nazwa')
    readonly_fields = ('data_rejestracji',)
    actions = ['zatwierdz_zgloszenia', 'odrzuc_zgloszenia']

    def bilans_bramek(self, obj):
        return f"{obj.bramki_zdobyte}:{obj.bramki_stracone}"
    bilans_bramek.short_description = 'Bramki'

    def zatwierdz_zgloszenia(self, request, queryset):
        updated = queryset.update(status='zatwierdzona')
        self.message_user(request, f"Zatwierdzono {updated} zgłoszeń")
    zatwierdz_zgloszenia.short_description = "Zatwierdź zgłoszenia"

    def odrzuc_zgloszenia(self, request, queryset):
        updated = queryset.update(status='odrzucona')
        self.message_user(request, f"Odrzucono {updated} zgłoszeń")
    odrzuc_zgloszenia.short_description = "Odrzuć zgłoszenia"

@admin.register(zawodnik)
class ZawodnikAdmin(admin.ModelAdmin):
    list_display = ('imie', 'nazwisko', 'id_druzyny', 'pozycja', 'numer_koszulki', 'data_urodzenia', 'zdjecie')
    list_filter = ('pozycja', 'id_druzyny')
    search_fields = ('imie', 'nazwisko', 'id_druzyny__nazwa')
    list_select_related = ('druzyna',)

    def zdjecie(self, obj):
        if obj.zdjecie_url:
            return format_html('<img src="{}" width="50" height="50" />', obj.zdjecie_url)
        return "-"
    zdjecie.short_description = 'Zdjęcie'

class WydarzenieInline(admin.TabularInline):
    model = wydarzenie
    extra = 0
    fields = ('minuta', 'typ', 'id_zawodnika', 'id_druzyny', 'komentarz')
    raw_id_fields = ('id_zawodnika',)

@admin.register(mecz)
class MeczAdmin(admin.ModelAdmin):
    inlines = [WydarzenieInline]
    list_display = ('nazwa_meczu', 'id_zawodu', 'id_kolejki', 'data_meczu', 'status', 'wynik')
    list_filter = ('status', 'id_zawodu', 'id_kolejki')
    search_fields = ('druzyna_gospodarz__druzyna__nazwa', 'druzyna_gosc__druzyna__nazwa')
    readonly_fields = ()
    actions = ['rozpocznij_mecze', 'zakoncz_mecze']

    def nazwa_meczu(self, obj):
        return f"{obj.druzyna_gospodarz.druzyna.nazwa} vs {obj.druzyna_gosc.druzyna.nazwa}"
    nazwa_meczu.short_description = 'Mecz'

    def wynik(self, obj):
        return f"{obj.wynik_gospodarz}:{obj.wynik_gosc}"
    wynik.short_description = 'Wynik'

    def rozpocznij_mecze(self, request, queryset):
        updated = queryset.update(status='rozpoczety')
        self.message_user(request, f"Rozpoczęto {updated} meczów")
    rozpocznij_mecze.short_description = "Rozpocznij mecze"

    def zakoncz_mecze(self, request, queryset):
        updated = queryset.update(status='zakonczony')
        self.message_user(request, f"Zakończono {updated} meczów")
    zakoncz_mecze.short_description = "Zakończ mecze"

@admin.register(wydarzenie)
class WydarzenieAdmin(admin.ModelAdmin):
    list_display = ('id_meczu', 'typ', 'minuta', 'id_zawodnika', 'id_druzyny')
    list_filter = ('typ', 'id_meczu')
    search_fields = ('id_zawodnika__imie', 'id_zawodnika__nazwisko', 'komentarz')
    raw_id_fields = ('id_zawodnika', 'id_meczu')

@admin.register(powiadomienie)
class PowiadomienieAdmin(admin.ModelAdmin):
    list_display = ('id_uzytkownika', 'typ', 'tresc_skrocona', 'data_wyslania', 'przeczytane')
    list_filter = ('typ', 'przeczytane', 'data_wyslania')
    search_fields = ('tresc', 'id_uzytkownika__email')
    readonly_fields = ('data_wyslania',)
    actions = ['oznacz_jako_przeczytane', 'oznacz_jako_nieprzeczytane']

    def tresc_skrocona(self, obj):
        return obj.tresc[:50] + '...' if len(obj.tresc) > 50 else obj.tresc
    tresc_skrocona.short_description = 'Treść'

    def oznacz_jako_przeczytane(self, request, queryset):
        updated = queryset.update(przeczytane=True)
        self.message_user(request, f"Oznaczono {updated} powiadomień jako przeczytane")
    oznacz_jako_przeczytane.short_description = "Oznacz jako przeczytane"

    def oznacz_jako_nieprzeczytane(self, request, queryset):
        updated = queryset.update(przeczytane=False)
        self.message_user(request, f"Oznaczono {updated} powiadomień jako nieprzeczytane")
    oznacz_jako_nieprzeczytane.short_description = "Oznacz jako nieprzeczytane"