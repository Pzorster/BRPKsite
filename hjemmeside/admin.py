from django.contrib import admin
from .models import *
from django.utils.formats import date_format

# Models registered in a simple way

# Part 1.1
admin.site.register(TypeAktivitet)
admin.site.register(StedAktivitet)
admin.site.register(MalgruppeAktivitet)
admin.site.register(DatoerSomUtgar)

# Part 1.2
admin.site.register(Personell)
admin.site.register(Rolle)
admin.site.register(AktivitetPersonell)

# Part 2
admin.site.register(Medlem)
admin.site.register(MeldtInteresse)
admin.site.register(KontakterForening)

# Part 3
admin.site.register(Oppmote)
admin.site.register(KontaktListe)
admin.site.register(TimeListePersonell)


# More complex representation and processing of models

# Part 1.3
# Inline model for AktivitetPersonell
class AktivitetPersonellInline(admin.TabularInline):
    model = AktivitetPersonell
    extra = 1

class AktivitetAdmin(admin.ModelAdmin):
    list_display = ['type_aktivitet', 'sted', 'malgruppe', 'oppstart', 'slutt', 'tidsrom', 'antall_ganger', 'pris', 'get_ansvars_personer', 'get_datoer_som_utgar']
    list_filter = ('oppstart', 'slutt', 'sted__omrade')
    search_fields = ['sted__omrade', 'malgruppe__alder_eller_klasse']
    inlines = [AktivitetPersonellInline]
    filter_horizontal = ['datoer_som_utgar']

    def tidsrom(self, obj):
        return f"{date_format(obj.kl_start, 'H:i')} - {date_format(obj.kl_slutt, 'H:i')}"
    tidsrom.short_description = "Tidsrom"

    def get_ansvars_personer(self, obj):
        # Get all related AktivitetPersonell objects for this Aktivitet
        personell_relations = obj.aktivitetpersonell_set.select_related('personell').all()
        
        # Format each relation to include role if available
        formatted_relations = []
        for relation in personell_relations:
            if relation.rolle:
                formatted_relations.append(f"{relation.personell} ({relation.rolle})")
            else:
                formatted_relations.append(f"{relation.personell}")
                
        return ", ".join(formatted_relations) if formatted_relations else "-"
    get_ansvars_personer.short_description = "Ansvars Personer"

    def get_datoer_som_utgar(self, obj):
        return ", ".join([str(dato) for dato in obj.datoer_som_utgar.all()]) or "-"
    get_datoer_som_utgar.short_description = "Datoer Som Utgår"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            'datoer_som_utgar', 
            'aktivitetpersonell_set__personell'
        )

admin.site.register(Aktivitet, AktivitetAdmin)

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
