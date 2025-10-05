from django.contrib import admin
from .models import *
from django.utils.formats import date_format
from django.utils.html import format_html
from django.urls import path, reverse
from django.http import HttpResponseRedirect

# Info 1: tabels admins don't need to see usually


# Info 2: Admin site cosmetics
admin.site.site_header = "Bergen Parkour"
admin.site.site_title = "Bergen Parkour Portal"
admin.site.index_title = "Admin Side"


# Info 3: No extra definition needed
admin.site.register(TypeAktivitet)
admin.site.register(StedAktivitet)
admin.site.register(MalgruppeAktivitet)
admin.site.register(DatoerSomUtgar)
admin.site.register(GenerellKursInfo)

admin.site.register(Rolle)

admin.site.register(ForesporselKategori)
admin.site.register(ForeningInfo)
admin.site.register(Bilde)

# Info 4: Small aditional function needed
class PersonellAdmin(admin.ModelAdmin):
    search_fields = ["fornavn", "etternavn"]

admin.site.register(Personell, PersonellAdmin)


class PersonellRolleAdmin(admin.ModelAdmin):
    list_filter = ("rolle", )
    search_fields = ["personell__fornavn", "personell__etternavn"]

admin.site.register(PersonellRolle, PersonellRolleAdmin)


class KundeKontaktAdmin(admin.ModelAdmin):
    list_display = ('navn', 'kategori', 'dato', 'fulgt_opp')
    list_filter = ('kategori', 'fulgt_opp', 'dato')
    ordering = ('-dato',)

admin.site.register(KundeKontakt, KundeKontaktAdmin)

class MedlemAdmin(admin.ModelAdmin):
    list_display = ('fornavn', 'etternavn', 'alder', 'hoved_kontakt_tlf', 'post_nummer')
    search_fields = ['fornavn', 'etternavn', 'alder', 'hoved_kontakt_tlf', 'kontakt2_tlf', 'kontakt3_tlf', 'post_nummer']
    readonly_fields = ['alder']

admin.site.register(Medlem, MedlemAdmin)


class AktivitetAdmin(admin.ModelAdmin):
    readonly_fields = ['antall_ganger', 'datoer','ledige_plasser_display']
    list_display = ['sted', 'malgruppe', 'start_dato', 'type_aktivitet','ledige_plasser_display']
    list_filter = ['sted', 'type_aktivitet', 'malgruppe']

    def ledige_plasser_display(self, obj):
        ledige = obj.ledige_plasser
        if ledige <= 0:
            return f"Venteliste: {abs(ledige)}"
        return str(ledige)
    ledige_plasser_display.short_description = 'Ledige plasser'
admin.site.register(Aktivitet)


# Part 3 - Requires some more functionality
