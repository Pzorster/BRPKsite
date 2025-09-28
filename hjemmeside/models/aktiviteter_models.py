from django.core.validators import RegexValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
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

    def __str__(self):
        return self.type_aktivitet

    class Meta:
        verbose_name = "Type aktivitet"
        verbose_name_plural = "Aktivitetsinfo: Type aktivtet"


class StedAktivitet(models.Model):
    """
    Representerer et sted vi har en aktivitet og har informasjon om vi evt. samrabeider med noen der.
    
    Brukes av:
    Aktivitet - hvilket sted aktiviteten skjer.
    """
    omrade = models.CharField(max_length=40)
    oppmote_sted = models.TextField()
    # Temporary: Solved by showing a help text. Should be changed in the future.
    samarbeids_partnere = models.JSONField(
        blank=True,
        default=list,
        help_text= """
        Må formateres som JSON. Anbefalt format [{"Info1": "Noe om de", "Kontaktinfo1": "Person: tlf"} , {"Info2": "Noe", "K2": "P:t"}]
        """
    )

    def __str__(self):
        return self.omrade

    class Meta:
        verbose_name = "Sted for aktivitet"
        verbose_name_plural = "Aktivitetsinfo: Sted for aktivitet"

# Future 1: The format/categorise could be different in the future, but right now this seems like the most viable option.
class MalgruppeAktivitet(models.Model):
    """
    Kobler en målgrupp vi har sammen med aktivitets nivået vi tilbyr de.
    
    Brukes av:
    Aktivitet - hvem som deltar på aktiviteten.
    """
    alder_eller_klasse = models.CharField(max_length=20, verbose_name="Alder/Kl")
    vanskelighetsgrad_eller_formal = models.CharField(max_length=20, verbose_name="Vanskelighetsgrad/Formål")

    def __str__(self):
        return f"{self.alder_eller_klasse} - {self.vanskelighetsgrad_eller_formal}"

    class Meta:
        verbose_name = "Målgruppe for aktivitet"
        verbose_name_plural = "Aktivitetsinfo: Målgruppe for aktivitet"


class DatoerSomUtgar(models.Model):
    """
    Viser datoer hvor aktiviteten utgår. Ofte grunnet helligdager.
    
    Brukes av:
    Aktivitet - når aktiviteten ikke skjer.
    """
    dato = models.DateField(unique=True)
    begrunnelse = models.CharField(max_length=100)

    def __str__(self):
        # Info: Formatert for å ikke vise årstallet ved visning.
        formattert_dato = self.dato.strftime('%d %b')
        return f"{formattert_dato} - {self.begrunnelse}"

    class Meta:
        ordering = ['dato']
        verbose_name = "Datoer som utgår"
        verbose_name_plural = "Aktivitetsinfo: Datoer som utgår"

class GenerellKursInfo(models.Model):
    """
    Generell informasjon brukere får før påmelding oppdelt atomisk.

    Brukes av:
    Aktivitet - informasjon som skal vises ved påmelding.
    """

    # Current 1: reconsider how you want to track these fields. They should have ID and maybe category?
    informasjon = models.JSONField()
    i_bruk = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Informasjon om kursene"
        verbose_name_plural = "Informasjon om kursene"

class Aktivitet(models.Model):
    """
    All nødvendig informasjon om en spesifikk aktivitet. Diverse ForeignKeys.
    
    Brukes av:
    MedlemPameldt - Oversikt over hvilken medlemmer som går på hvilken aktivitet.
    AktivitetsDatoer - Oversikt over alle datoene en aktivitet går
    """

    # Current 1: reconsider the whole thing now that the pipeline is different.
    # Current 2: Filter/sorter på en del av attr.
    # Current 3: Gå gjennom valideringen
    # Current 4: (DOnt remember this)Ta en endelig vurdering på Choice formateringen du har lyst å kjøre.
    type_aktivitet = models.ForeignKey(TypeAktivitet, on_delete=models.PROTECT)
    sted = models.ForeignKey(StedAktivitet, on_delete=models.PROTECT)
    malgruppe = models.ForeignKey(MalgruppeAktivitet, on_delete=models.PROTECT)
    personell_rolle = models.ManyToManyField(PersonellRolle)
    datoer_som_utgar = models.ManyToManyField(DatoerSomUtgar)
    start_dato = models.DateField()
    slutt_dato = models.DateField(editable=False, null=True, blank=True)
    kl_start = models.TimeField()
    kl_slutt = models.TimeField()
    antall_ganger = models.PositiveIntegerField()
    antall_plasser = models.PositiveIntegerField()
    ledige_plasser = models.PositiveIntegerField()
    pris_vanlig = models.PositiveIntegerField()
    pris_drop_in = models.PositiveIntegerField()
    dag_interval = models.PositiveIntegerField()
    merknader = models.TextField(blank=True, default="")

    # Current 5: Drop this in favour of having an archiveing function that removes them once they are past their end date?
    # Tids statusen for aktiviteten
    STATUS_KOMMENDE = 'Kommende'
    STATUS_PAGAENDE = 'Pågående'
    STATUS_AVSLUTTET = 'Avsluttet'
    
    status_oppstart = models.CharField(
        max_length=20,
        default=STATUS_KOMMENDE,
        choices=[
            (STATUS_KOMMENDE, 'Kommende'),
            (STATUS_PAGAENDE, 'Pågående'),
            (STATUS_AVSLUTTET, 'Avsluttet'),
        ]
    )

    # Regner ut tids status for aktiviteten
    @property
    def current_status(self):
        today = timezone.now().date()
        if today < self.start_dato:
            return self.STATUS_KOMMENDE
        elif today <= self.slutt_dato:
            return self.STATUS_PAGAENDE
        else:
            return self.STATUS_AVSLUTTET

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
        
        dag_nummer = self.start_dato.weekday()  # Returns 0-6 (Monday=0)
        return norske_ukedager[dag_nummer]
    
    # Move 1: This should be in the påmeldteDeltager tabel
    # Regner ut ledige plasser for aktiviteteten
    @property
    def current_ledige_plasser(self):
        # Real-time calculation when accessed
        opptatte_plasser = self.pameldte_deltagere.count()
        return max(0, self.antall_plasser - opptatte_plasser)
        
    @property
    def display_price(self):
        """Returnerer pris på en mer forståelig måte for nordmenn"""
        if self.pris_vanlig == 0:
            return "gratis"
        return f"{self.pris_vanlig} kr"
    
    # Husker ikke formålet
    def update_status(self):
        """Update the stored status field to current status"""
        current = self.current_status
        if self.status_oppstart != current:
            self.status_oppstart = current
            self.save(update_fields=['status_oppstart'])

    def save(self, *args, **kwargs):
        is_new = not self.pk  # Check if this is a new object
        needs_recalculation = not self.slutt_dato or any(
            field in kwargs.get('update_fields', []) 
            for field in ['start_dato', 'dag_interval', 'antall_ganger']
        )
        
        if not self.ledige_plasser:
            self.ledige_plasser = self.antall_plasser

        # First save for new objects to get a PK
        if is_new:
            super().save(*args, **kwargs)
        
        if (needs_recalculation or is_new) and self.pk:  # This condition is missing in your code
        # Calculate end date if needed
            excluded_dates = list(self.datoer_som_utgar.values_list('dato', flat=True).distinct())
            
            # Clear existing dates if we're recalculating
            if not is_new:
                self.aktivitet_datoer.all().delete()
        
            # Generate course dates
            course_dates = []
            current_date = self.start_dato
            dates_generated = 0
            
            while dates_generated < self.antall_ganger:
                # Skip excluded dates
                if current_date not in excluded_dates:
                    course_dates.append(AktivitetDatoer(aktivitet=self, dato=current_date))
                    dates_generated += 1
                
                # Move to next potential date
                current_date += timedelta(days=self.dag_interval)
            
            # Save all dates at once
            AktivitetDatoer.objects.bulk_create(course_dates)
            
            # Set slutt_dato to the last course date
            last_date = max(cd.dato for cd in course_dates)
            self.slutt_dato = last_date
            
            # Save with just the updated field
            super().save(update_fields=['slutt_dato'])
        elif not is_new:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sted} {self.malgruppe}"

    class Meta:
        verbose_name = "Aktivitet"
        verbose_name_plural = "Aktiviteter"

# Move 1: This should be automtically generated by aktiviteter
class AktivitetDatoer(models.Model):
    """
    Oversikt over alle datoer en aktivitet(Aktivitet) går på.
    
    Automatisk generert og justert mellom tabell som ikke er synlig i Admin.
    
    Brukes av:
    DeltagerOppmote - for datoer deltagere skal noteres tilstedeværelse på.
    PersonellOppmote - for datoer personell skal noteres tilstedeværelse på.
    """
    aktivitet = models.ForeignKey(Aktivitet, on_delete=models.PROTECT, related_name='aktivitet_datoer')
    dato = models.DateField()
    
    class Meta:
        ordering = ['dato']
        unique_together = ['aktivitet', 'dato']
        verbose_name = "Aktivitets dato"
        verbose_name_plural = "Aktivitetsinfo: Aktivitets datoer"
    
    def __str__(self):
        return f"{self.aktivitet} {self.dato}"
    
    class Meta:
        verbose_name = "Datoer for aktivitet"
        verbose_name_plural = "Aktivitetsinfo: Datoer for aktiviteten"

