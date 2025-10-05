from django.db import models
from datetime import timedelta
from .validators import kun_tall_validator
from .ansatt_models import PersonellRolle


class TypeAktivitet(models.Model): 
    """
    Definerer ulike type aktiviter som vi har.
    
    Brukes av:
    Aktivitet - hvilken aktivtets type det er.
    """
    type_aktivitet = models.CharField(max_length=40)

    class Meta:
        verbose_name = "Type aktivitet"
        verbose_name_plural = "Aktivitetsinfo: Type aktivtet"

    def __str__(self):
        return self.type_aktivitet


class StedAktivitet(models.Model):
    """
    Representerer et sted vi har en aktivitet og har informasjon om vi evt. samrabeider med noen der.
    
    Brukes av:
    Aktivitet - hvilket sted aktiviteten skjer.
    """
    omrade = models.CharField(max_length=40)
    oppmote_sted = models.TextField()
    # Temporary 1: Solved by showing a help text. Should be changed in the future.
    samarbeids_partnere = models.JSONField(
        blank=True,
        default=list,
        help_text= """
        Må formateres som JSON. Anbefalt format [{"Info1": "Noe om de", "Kontaktinfo1": "Person: tlf"} , {"Info2": "Noe", "K2": "P:t"}]
        """
    )

    class Meta:
        verbose_name = "Sted for aktivitet"
        verbose_name_plural = "Aktivitetsinfo: Sted for aktivitet"

    def __str__(self):
        return self.omrade


# Future 1: The format/categorise could be different in the future, but right now this seems like the most viable option.
class MalgruppeAktivitet(models.Model):
    """
    Kobler en målgrupp vi har sammen med aktivitets nivået vi tilbyr de.
    
    Brukes av:
    Aktivitet - hvem som deltar på aktiviteten.
    """
    alder_eller_klasse = models.CharField(max_length=20, verbose_name="Alder/Kl")
    vanskelighetsgrad_eller_formal = models.CharField(max_length=20, verbose_name="Vanskelighetsgrad/Formål")

    class Meta:
        verbose_name = "Målgruppe for aktivitet"
        verbose_name_plural = "Aktivitetsinfo: Målgruppe for aktivitet"
    
    def __str__(self):
        return f"{self.alder_eller_klasse} - {self.vanskelighetsgrad_eller_formal}"


class DatoerSomUtgar(models.Model):
    """
    Viser datoer hvor aktiviteten utgår. Ofte grunnet helligdager.
    
    Brukes av:
    Aktivitet - når aktiviteten ikke skjer.
    """
    dato = models.DateField(unique=True)
    begrunnelse = models.CharField(max_length=100)

    class Meta:
        ordering = ['dato']
        verbose_name = "Datoer som utgår"
        verbose_name_plural = "Aktivitetsinfo: Datoer som utgår"

    def __str__(self):
        """Formatert for å ikke vise årstallet ved visning."""
        formattert_dato = self.dato.strftime('%d %b')
        return f"{formattert_dato} - {self.begrunnelse}"


class GenerellKursInfo(models.Model):
    """
    Generell informasjon brukere får før påmelding oppdelt atomisk.

    Brukes av:
    Aktivitet - informasjon som skal vises ved påmelding.
    """
    beskrivelse = models.CharField(max_length=40)
    informasjon = models.TextField()
    i_bruk = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Informasjon om kursene"
        verbose_name_plural = "Informasjon om kursene"

class Aktivitet(models.Model):
    """
    All nødvendig informasjon om en spesifikk aktivitet.

    Henter informasjon ifra:
    TypeAktivitet - Hva slags type aktivitet det er.
    Sted - Informajon om stedet aktiviteten foregår på.
    Malgruppe - Hvilken malgruppe er aktiviteten for.
    GenerellInfo - Informasjon som deltagere skal få i påmeldingsskjema.
    PersonellRolle - Hvem er det ansvarlige personene som leder aktiviteten.
    DatoerSomUtgar - Datoer aktiviteten ikke går. Som oftest grunnet skoleruten.
    
    Brukes av:
    MedlemPameldt - Oversikt over hvilken medlemmer som går på hvilken aktivitet.
    AktivitetsDatoer - Oversikt over alle datoene en aktivitet går
    """
    type_aktivitet = models.ForeignKey(TypeAktivitet, on_delete=models.PROTECT)
    sted = models.ForeignKey(StedAktivitet, on_delete=models.PROTECT)
    malgruppe = models.ForeignKey(MalgruppeAktivitet, on_delete=models.PROTECT)
    generell_info = models.ManyToManyField(GenerellKursInfo)
    personell_rolle = models.ManyToManyField(PersonellRolle)
    datoer_som_utgar = models.ManyToManyField(DatoerSomUtgar)
    start_dato = models.DateField()
    slutt_dato = models.DateField()
    kl_start = models.TimeField()
    kl_slutt = models.TimeField()
    antall_ganger = models.PositiveIntegerField(null=True, blank=True)
    antall_plasser = models.PositiveIntegerField()
    pris_vanlig = models.PositiveIntegerField()
    pris_drop_in = models.PositiveIntegerField()
    en_gang_i_uken = models.BooleanField(default=True)
    datoer = models.JSONField(default=list, blank=True)
    merknader = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "Aktivitet"
        verbose_name_plural = "Aktiviteter"

    def __str__(self):
        return f"{self.sted} {self.malgruppe}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.generate_dates()
        super().save(update_fields=['datoer', 'antall_ganger'])

    @property
    def ledige_plasser(self):
        pameldte = self.medlempameldt_set.filter(
            status_pamelding='pameldt',
        ).count()
        return self.antall_plasser - pameldte
    
    @property
    def ukedag(self):
        """Returns Norwegian weekday name for start_dato"""
        norske_ukedager = [
            'Mandag',    # 0
            'Tirsdag',   # 1
            'Onsdag',    # 2
            'Torsdag',   # 3
            'Fredag',    # 4
            'Lørdag',    # 5
            'Søndag'     # 6
        ]
        dag_nummer = self.start_dato.weekday()
        return norske_ukedager[dag_nummer]
            
    @property
    def display_price(self):
        """Returnerer pris på en mer forståelig måte for nordmenn"""
        if self.pris_vanlig == 0:
            return "gratis"
        return f"{self.pris_vanlig} kr"

    def generate_dates(self):
        """Generer kursdatoer til bruk på oppmøtelistene"""
        self.datoer = []
        dato = self.start_dato

        if self.en_gang_i_uken:
            interval = 7
        else:
            interval = 1

        ekskludterte_datoer = set(self.datoer_som_utgar.values_list('dato', flat=True))
        while dato <= self.slutt_dato:
            if dato not in ekskludterte_datoer:
                self.datoer.append(dato.isoformat())
            dato += timedelta(days=interval)
        antall_ganger = len(self.datoer)
        self.antall_ganger = antall_ganger