from .aktiviteter_models import *
from .ansatt_models import *
from .medlemmer_models import *
from .site_models import *

# Because for the validator to work it cant only be imported in the other model files, it also needs to be here?
from .validators import *

# I dont understand how this works, but ill start with it

__all__ = [

]

from django.core.validators import RegexValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from datetime import timedelta

# The sub-models hold the core/entity models
# The main model will hold assosiative/junction tables representing the dynamic relation between the models




class MedlemPameldt(models.Model):

# Kanskje drop-in skal endres til BetalingsType og sånn blir deltagere fordelt på betalignstabeller?
# Legge til rabatt attr her.
    """
    Oversikt over hvilken medlemmer(Medlem) som er påmeldt hvilken aktiviteter(Aktivitet).
    
    Brukes av:
    Aktiviteter - for å sjekke ledige plasser.
    DeltagerOppmote - for å sjekke hvilken deltagere det skal sjekkes oppmøte på.

    """
    aktivitet = models.ForeignKey(Aktivitet, on_delete = models.PROTECT, related_name= "pameldte_deltagere")
    medlem = models.ForeignKey(Medlem, on_delete = models.PROTECT)
    drop_in = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.medlem} - {self.aktivitet}"
    
    class Meta:
        verbose_name = "Påmeldt deltager"
        verbose_name_plural = "Medlemsinfo: Deltager påmelding"

class BetalingsType(models.Model):

# Kanskje hele denne skal flyttes og brukes i MedlemPameldt for å sortere mellom standard, drop-in og støtte?
# Trenger den å være synlig admin side eller kan den være skjult i koden?
    """
    Måter folk kan betale for deltagelse på aktiviteter.
    
    Brukes av:
    Betalingstatus - for å sette hvordan deltagere har betalt.
    """
    navn = models.CharField(max_length=30)
    
    def __str__(self):
        return self.navn
    
    class Meta:
        verbose_name = "Betalingstype"
        verbose_name_plural = "Medlemsinfo: Betalingstyper"

class BetalingStatus(models.Model):

# Vil trenge et filter på status_betaling
# Rabatt flyttes til MedlemPameldt.
    """
    Oversikt over hvem som har betalt(MedlemPameldt.drop_in = False), hvor mye og hvordan(BetalingsType).
    Drop-in har egen tabell. Aktivitet tabel brukes for å regne ut hvor mye de skal betale.
    
    Planlagt brukt i flere tabeller/funksjoner forbi fase 1.
    """
    medlem_pameldt = models.ForeignKey(MedlemPameldt, on_delete=models.PROTECT)
    type_betaling = models.ForeignKey(BetalingsType, on_delete=models.PROTECT)
    original_pris = models.PositiveIntegerField()
    rabatt = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(1)], help_text="Prosentrabatt: skriv in et tall mellom 0 og 1. Eks. 0.70 = 70%.")
    endelig_pris = models.PositiveIntegerField()
    status_betaling = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.medlem_pameldt} - Status: {self.status_betaling}"

    def save(self, *args, **kwargs):

        # Regner ut en pris basert på en prosent rabatt
        self.original_pris = self.medlem_pameldt.aktivitet.pris_vanlig
        self.endelig_pris = self.original_pris*(1-self.rabatt)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Betaling status"
        verbose_name_plural = "Medlemsinfo: Betaling status"



class DeltagerOppmote(models.Model):

# Hadde vært fint å kunne filterer etter aktivtet og så vise en oppmøte tabell der 1 medlem kobles til 1 rad der dens oppmøte vises
    """
    Oversikt over oppmøte til aktivitets deltagere(MedlemPameldt) på spesifikke datoer(AktivitetDatoer).
    
    Brukes av:
    BetalingStatusDropIn - datoer deltager er tilstede skapes i tabellen for å kontrollerer betaling.
    """
    aktivitet_datoer = models.ForeignKey(AktivitetDatoer, on_delete=models.PROTECT)
    medlem_pameldt = models.ForeignKey(MedlemPameldt, on_delete=models.PROTECT)
    tilstede = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.medlem_pameldt.medlem} {self.aktivitet_datoer.dato}"
    
    class Meta:
        verbose_name = "Deltager oppmøte"
        verbose_name_plural = "Medlemsinfo: Deltager oppmøte"

class PersonellOppmote(models.Model):

# Denne vil trenge en del filter funskjoner basert på diverse foreldre og på utbetalt_lonn.
# I tilegg til en knapp for å bekrefte utbetalelse før hele systemet er på plass.
    """
    Oversikt over hvem(PersonellRolle) som jobbet på hvilken aktivitet på en spesifikk dato(AktivitetDatoer).
    
    Planlagt brukt i flere tabeller forbi fase 1.
    """
    aktivitet_datoer = models.ForeignKey(AktivitetDatoer, on_delete=models.PROTECT)
    personel_rolle = models.ForeignKey(PersonellRolle, on_delete=models.PROTECT)
    utbetalt_lonn = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.personel_rolle} {self.aktivitet_datoer} - Status utbetaling: {self.utbetalt_lonn}"

    class Meta:
        verbose_name = "Personell oppmøte"
        verbose_name_plural = "Personellinfo: Personell oppmøte"

class BetalingStatusDropIn(models.Model):

# Vil trenge en filter funksjon på status_betaling, deltager navn
# Vil og trenge en generator funskjon som oppdatereres ukentlig basert på x
# Skal rabatt funksjonene legges i MedlemPameldt isteden og så heller brukes til utregning i BetalingStatus og BetalingStatusDropIn?
    """
    Oversikt over alle(MedlemPameldt.drop_in = True) som betaler drop-in og hvilken datoer de har vært tilstede(DeltagerOppmote) og betalt for.
    
    Planlagt brukt i flere tabeller forbi fase 1.
    """
    deltager_oppmote = models.ForeignKey(DeltagerOppmote, on_delete=models.PROTECT)
    dato = models.DateField()
    original_pris = models.PositiveIntegerField()
    rabatt = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(1)], help_text="Prosentrabatt: skriv in et tall mellom 0 og 1. Eks. 0.70 = 70%.")
    endelig_pris = models.PositiveIntegerField()
    status_betaling = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.deltager_oppmote} - Status: {self.status_betaling}"

    def save(self, *args, **kwargs):

        # Regner ut en pris basert på en prosent rabatt
        self.original_pris = self.deltager_oppmote.aktivitet_datoer.aktivitet.pris_drop_in
        self.endelig_pris = self.original_pris*(1-self.rabatt)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Betaling status drop-in"
        verbose_name_plural = "Medlemsinfo: Betaling status drop-in"



# Legg til en tilskudd/støtte tabell forbi fase 1
# Forbi en viss fase legg inn statistikk funksjone