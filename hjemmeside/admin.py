from django.contrib import admin
from .models import *
from django.utils.formats import date_format
from django.utils.html import format_html
from django.urls import path, reverse
from django.http import HttpResponseRedirect


# Questions: What do you want to see when? What needs to be searchable/filtreable? What shouldnt be cahngable?



# Part 0 - tabels admins don't need to see usually


# Admin site cosmetics
admin.site.site_header = "Bergen Parkour"
admin.site.site_title = "Bergen Parkour Portal"
admin.site.index_title = "Admin Side"

# Part 1 - No extra definition needed
admin.site.register(TypeAktivitet)
admin.site.register(StedAktivitet)
admin.site.register(MalgruppeAktivitet)
admin.site.register(DatoerSomUtgar)
admin.site.register(Rolle)
admin.site.register(ForesporselKategori)
admin.site.register(ForeningInfo)
admin.site.register(Bilde)
admin.site.register(GenerellKursInfo)

# Part 2 - Small aditional functions
class PersonellAdmin(admin.ModelAdmin):
    search_fields = ["fornavn", "etternavn"]

admin.site.register(Personell, PersonellAdmin)


class PersonellRolleAdmin(admin.ModelAdmin):
    list_filter = ("rolle", )
    search_fields = ["personell__fornavn", "personell__etternavn"]

admin.site.register(PersonellRolle, PersonellRolleAdmin)



# Skal endres
admin.site.register(Medlem)

class KundeKontaktAdmin(admin.ModelAdmin):
    list_display = ('navn', 'kategori', 'dato', 'fulgt_opp')
    list_filter = ('kategori', 'fulgt_opp', 'dato')
    ordering = ('-dato',)

admin.site.register(KundeKontakt, KundeKontaktAdmin)
admin.site.register(MedlemPameldt)
admin.site.register(BetalingsType)
admin.site.register(BetalingStatus)
admin.site.register(AktivitetDatoer)
admin.site.register(DeltagerOppmote)
admin.site.register(PersonellOppmote)
admin.site.register(BetalingStatusDropIn)


# Part 3 - Requires some more functionality
admin.site.register(Aktivitet)
# # Should be searchable
# admin.site.register(Medlem)

# # Part 2
# admin.site.register(KontakterForening)

# # Part 3
# admin.site.register(Oppmote)
# admin.site.register(KontaktListe)
# admin.site.register(TimeListePersonell)


# # More complex representation and processing of models

# # Part 1.3
# # Inline model for AktivitetPersonell
# class AktivitetPersonellInline(admin.TabularInline):
#     model = AktivitetPersonell
#     extra = 1

# class AktivitetAdmin(admin.ModelAdmin):
#     list_display = ['type_aktivitet', 'sted', 'malgruppe', 'oppstart', 'slutt', 'tidsrom', 'antall_ganger', 'pris', 'get_ansvars_personer', 'get_datoer_som_utgar']
#     list_filter = ('oppstart', 'slutt', 'sted__omrade')
#     search_fields = ['sted__omrade', 'malgruppe__alder_eller_klasse']
#     inlines = [AktivitetPersonellInline]
#     filter_horizontal = ['datoer_som_utgar']

#     def tidsrom(self, obj):
#         return f"{date_format(obj.kl_start, 'H:i')} - {date_format(obj.kl_slutt, 'H:i')}"
#     tidsrom.short_description = "Tidsrom"

#     def get_ansvars_personer(self, obj):
#         # Get all related AktivitetPersonell objects for this Aktivitet
#         personell_relations = obj.aktivitetpersonell_set.select_related('personell').all()
        
#         # Format each relation to include role if available
#         formatted_relations = []
#         for relation in personell_relations:
#             if relation.rolle:
#                 formatted_relations.append(f"{relation.personell} ({relation.rolle})")
#             else:
#                 formatted_relations.append(f"{relation.personell}")
                
#         return ", ".join(formatted_relations) if formatted_relations else "-"
#     get_ansvars_personer.short_description = "Ansvars Personer"

#     def get_datoer_som_utgar(self, obj):
#         return ", ".join([str(dato) for dato in obj.datoer_som_utgar.all()]) or "-"
#     get_datoer_som_utgar.short_description = "Datoer Som Utgår"

#     def get_queryset(self, request):
#         return super().get_queryset(request).prefetch_related(
#             'datoer_som_utgar', 
#             'aktivitetpersonell_set__personell'
#         )

# admin.site.register(Aktivitet, AktivitetAdmin)

# class MeldtInteresseAdmin(admin.ModelAdmin):
#     list_display = ['oppsummert', 'dato', 'fulgt_opp'] #'send_email_button'
#     list_filter = ('dato', 'fulgt_opp')
#     readonly_fields = ('dato', 'oppsummert', 'detaljer')

    # This is code for automatically opening up a mail to send it. This function ill add much later.

    # def send_email_button(self, obj):
    #     """Custom button to send email response"""
    #     # Only render button if not already followed up
    #     if not obj.fulgt_opp:
    #         return format_html(
    #             '<a class="button" href="{}">Send Epost</a>',
    #             reverse('admin:mark_as_followed_up', args=[obj.pk])  # Changed URL name
    #         )
    #     return "Epost sendt"
    # send_email_button.short_description = "Send Epost?"
    
    # def get_urls(self):
    #     """Add custom URL for email sending"""
    #     urls = super().get_urls()
    #     custom_urls = [
    #         path(
    #             'mark-as-followed/<int:pk>/',  # URL pattern
    #             self.admin_site.admin_view(self.send_email_view),
    #             name='mark_as_followed_up',  # URL name used in reverse()
    #         ),
    #     ]
    #     return custom_urls + urls
    
    # def send_email_view(self, request, pk):
    #     obj = self.get_object(request, pk)
        
    #     # Instead of sending email, just log it
    #     print(f"Would send email to {obj.mail} about {obj.oppsummert}")
        
    #     # Mark as followed up
    #     obj.fulgt_opp = True
    #     obj.save()
        
    #     self.message_user(request, f"Marked {obj.oppsummert} as followed up")
    #     # Change this to your actual app name and model name
    #     return HttpResponseRedirect(reverse('admin:yourappname_meldtinteresse_changelist'))


# admin.site.register(MeldtInteresse, MeldtInteresseAdmin)

# from django.contrib import admin
# from .models import *
# from django.utils.formats import date_format




# # Models: TypeAktivitet, StedAktivitet, MalgruppeAktivitet, Personell, Aktivtet, DatoerSomUtgar



# admin.site.register(TypeAktivitet)
# admin.site.register(StedAktivitet)
# admin.site.register(MalgruppeAktivitet)
# admin.site.register(Personell)
# admin.site.register(DatoerSomUtgar)

# # Standard class that can be used to display all the fields of a db as a table
# # class AdminTableDisplay(admin.ModelAdmin):
# #     def __init__(self, model, admin_site):
# #         self.list_display = [field.name for field in model._meta.fields]
# #         super().__init__(model, admin_site)
# # def many_to_many_list_display(obj, related_field):
# #     if hasattr(obj, related_field):
# #         related_objects = getattr(obj, related_field).all()
# #         return ", ".join(str(item) for item in related_objects) if related_objects else "ur"
# #     return "test"

# # def many_to_many_list_display(obj, related_field):
# #     if hasattr(obj, related_field):
# #         related_objects = getattr(obj, related_field).all()
# #         print(f"DEBUG: {related_field} for {obj} -> {related_objects}")  
# #         return ", ".join(str(item) for item in related_objects) if related_objects else "EMPTY"
# #     return "MISSING"

# def many_to_many_list_display(obj, related_field):
#     print(f"DEBUG: Called many_to_many_list_display for {related_field} on {obj}")

#     if related_field == "ansvars_personer":
#         # Retrieve through intermediary model
#         related_objects = obj.aktivitetpersonell_set.all()
#         return ", ".join(str(item.personell) for item in related_objects) if related_objects else "EMPTY1"
    
#     if hasattr(obj, related_field):
#         related_objects = list(getattr(obj, related_field).all())
#         print(f"DEBUG: {related_field} for {obj} -> {related_objects}")
#         return ", ".join(str(item) for item in related_objects) if related_objects else "EMPTY"

#     return "MISSING"



# # class AktivitetPersonellInline(admin.TabularInline):
# #     model = AktivitetPersonell
# #     extra = 1  # Allows adding new entries directly in the admin

# # class AktivitetAdmin(admin.ModelAdmin):
# #     list_filter = ('oppstart', 'slutt')
# #     search_fields = ['sted__omrade']
# #     filter_horizontal = ['datoer_som_utgar']  # We remove ansvars_personer from filter_horizontal
# #     inlines = [AktivitetPersonellInline]  # Uses the inline form for ManyToMany

# #     def __init__(self, model, admin_site):
# #         self.list_display = [
# #             field.name for field in model._meta.fields if field.name not in ["id", "kl_start", "kl_slutt"]
# #         ]
# #         super().__init__(model, admin_site)
# #         self.list_display += ['tidsrom', 'dager_som_utgar', 'ansvars_personer'] 

# #     # def __init__(self, model, admin_site):
# #     #     self.list_display = [field.name for field in model._meta.fields if field.name not in ["id", "kl_start", "kl_slutt"]]
# #     #     super().__init__(model, admin_site)
# #     #     # self.list_display = self.list_display + ['tidsrom', 'dager_som_utgar', 'ansvars_personer']
# #     #     self.list_display = self.list_display + ['tidsrom', 'ansvars_personer']

# #     def tidsrom(self, obj):
# #         return f"{date_format(obj.kl_start, 'H:i')}_{date_format(obj.kl_slutt, 'H:i')}"

# #     def save_model(self, request, obj, form, change):
# #         super().save_model(request, obj, form, change)

# #     # def save_related(self, request, obj, form, formsets, change):
# #     #     super().save_related(request, obj, form, formsets, change)
# #     #     form.save_m2m()  # Ensures ManyToMany relationships are saved

# #     def dager_som_utgar(self, obj):
# #         return many_to_many_list_display(obj, "datoer_som_utgar")

# #     def ansvars_personer(self, obj):
# #         return many_to_many_list_display(obj, "ansvars_personer")
    
# #     def get_queryset(self, request):
# #         return super().get_queryset(request).prefetch_related('datoer_som_utgar', 'aktivitetpersonell_set__personell')


#     # def get_queryset(self, request):
#     #     return super().get_queryset(request).prefetch_related('datoer_som_utgar', 'ansvars_personer')
# class AktivitetAdmin(admin.ModelAdmin):
#     list_display = ['ansvars_personer']  # Force explicit listing

#     @admin.display(description="Ansvars Personer") 
#     def ansvars_personer(self, obj):
#         return many_to_many_list_display(obj, "ansvars_personer")

#     # def dager_som_utgar(self, obj):
#     #     return many_to_many_list_display(obj, "datoer_som_utgar")

#     def get_queryset(self, request):
#         return super().get_queryset(request).prefetch_related(
#             'datoer_som_utgar', 'aktivitetpersonell_set__personell'
#         )

# admin.site.register(Aktivitet, AktivitetAdmin)
# # class AktivitetAdmin(AdminTableDisplay):

# #     list_filter = ('oppstart', 'slutt')
# #     search_fields = ['sted__omrade']

# #     def klokkeslett(self, obj):
# #     return f"{date_format(obj.kl_start, 'H:i')} - {date_format(obj.kl_slutt, 'H:i')}"
    
# #     def dager_som_utgar_list(self, obj):
# #         return ", ".join([f"{d.dato.strftime('%d.%b')}" for d in obj.datoer_som_utgar.all()])
    
# #     list_display = list(AdminTableDisplay.list_display) + ['klokkeslett', 'dager_som_utgar_list']

# # admin.site.register(Aktivitet, AktivitetAdmin)
