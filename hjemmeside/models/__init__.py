from .aktiviteter_models import TypeAktivitet, StedAktivitet, MalgruppeAktivitet, DatoerSomUtgar, GenerellKursInfo, Aktivitet
from .ansatt_models import Rolle, Personell, PersonellRolle
from .medlemmer_models import Medlem
from .site_models import ForesporselKategori, KundeKontakt, Bilde, ForeningInfo
from .validators import kun_tall_validator
from django.db import models

# CORE
# The sub-models hold the core/entity models
# The main model will hold assosiative/junction tables representing the dynamic relation between the models

class BetalingRegistrering(models.Model):
    """
    Holder oversikt over betalinger som er gjennomført fra medlemmer.

    Henter informasjon ifra:
    Medlem - hvem betalingen gjelder

    Brukes av:
    MedlemPameldt - for å se hvem som har betalt.
    DropInBetaling - for å se hvem som har betalt.
    KunMedlemmer - for å se hvem som har betalt.
    """
    medlem = models.ForeignKey(Medlem, on_delete=models.PROTECT)
    belop = models.PositiveIntegerField()
    dato = models.DateTimeField(null=True, blank=True)
    betaling_status = models.CharField(
        max_length=20,
        choices=[
            ('venter', 'Venter på betaling'),
            ('godkjent', 'Godkjent'),
            ('feilet', 'Feilet'),
            ('refundert', 'Refundert'),
            ('kansellert', 'Kansellert')
        ],
        default='venter'
    )
    kvittering_url= models.URLField(blank=True)
    transaksjons_id = models.CharField(max_length=100, blank=True)
    betaling_formal = models.JSONField(default=list)

    class Meta:
        verbose_name = "Betaling fra medlem"
        verbose_name_plural = "Betalinger fra medlemmer"

    def __str__(self):
        return f"{self.medlem} - {self.belop} kr -{self.dato}"

class AktivitetskortetDeltager(models.Model):
    """
    Holder oversikt over brukere av aktivitetskortet og hvorvidt kortet deres er godkjent.

    Henter informasjon ifra:
    Medlem - hvem betalingen gjelder

    Brukes av:
    """
    medlem = models.ForeignKey(Medlem, on_delete=models.PROTECT)
    aktivitetskort_bilde1 = models.ImageField(upload_to='aktivitetskort/', blank=True, null=True)
    aktivitetskort_bilde2 = models.ImageField(upload_to='aktivitetskort/', blank=True, null=True)
    aktivitetskort_godkjent = models.BooleanField(default=False)

# Future 1: Maybe should be a verifier here that checks if someone is already signed-up when they try to submit their form?
class MedlemPameldt(models.Model):
    """
    Holder oversikt over hvem som er påmeldt hvilken aktivitet.

    Henter informasjon ifra:
    Medlem - Hvem dette gjelder.
    Aktivitet - Hvilken aktivitet det gjelder.
    BetalingRegistrering - Informasjon om gjennomført betaling.

    Brukes av:
    Aktivitet - for å kalkulere antall ledige plasser.
    DeltagerOppmote - for å hente informasjon om deltagere og datoene for aktiviteten.
    """
    aktivitet = models.ForeignKey(Aktivitet, on_delete=models.PROTECT)
    medlem = models.ForeignKey(Medlem, on_delete=models.PROTECT)
    dato_pameldt = models.DateTimeField(auto_now_add=True)
    status_pamelding = models.CharField(
        max_length=20,
        choices=[
            ('pameldt', 'Pameldt'),
            ('avmeldt', 'Avmeldt'),
            ('venteliste', 'Venteliste')
        ]
    )
    type_betaling = models.CharField(
        max_length=20,
        choices = [
            ('drop_in', 'Drop-In'),
            ('vanlig', 'Vanlig'),
            ('aktivitetskortet', 'Aktivitetskortet'),
            ('gratis', 'Gratis'),
            ('friplass', 'Friplass'),
            ('redusert betaling', 'Redusert Betaling')
        ]
    )
    # Current 1: added null/blank only for migrations
    betaling_registrert = models.ForeignKey(BetalingRegistrering, on_delete=models.PROTECT, null=True, blank=True)
    oppfolging_notater = models.TextField(blank=True)
    trenger_oppfolging = models.BooleanField(default=True)

class DropInBetaling(models.Model):
    """
    Holder oversikt over alle ganger en person med drop-in har deltatt og hvoridt de har betalt.

    Henter informasjon ifra:

    Brukes av:
    """
    pass

class KunMedlemmer(models.Model):
    """
    Holder oversikt over de som bare er medlemmer uten å delta på aktiviter som koster
    og for hvilket år kontigenten deres er betalt.

    Henter informasjon ifra:

    Brukes av:

    """
    pass


# klasse for fond midler inn og fond midler ut
# Output hva som er tilgjengelig, men man kan gå inn og se alt?

# class DeltagerOppmote(models.Model):

# # Hadde vært fint å kunne filterer etter aktivtet og så vise en oppmøte tabell der 1 medlem kobles til 1 rad der dens oppmøte vises
#     """
#     Oversikt over oppmøte til aktivitets deltagere(MedlemPameldt) på spesifikke datoer(AktivitetDatoer).
    
#     Brukes av:
#     BetalingStatusDropIn - datoer deltager er tilstede skapes i tabellen for å kontrollerer betaling.
#     """
#     aktivitet_datoer = models.ForeignKey(AktivitetDatoer, on_delete=models.PROTECT)
#     medlem_pameldt = models.ForeignKey(MedlemPameldt, on_delete=models.PROTECT)
#     tilstede = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.medlem_pameldt.medlem} {self.aktivitet_datoer.dato}"
    
#     class Meta:
#         verbose_name = "Deltager oppmøte"
#         verbose_name_plural = "Medlemsinfo: Deltager oppmøte"

# class PersonellOppmote(models.Model):

# # Denne vil trenge en del filter funskjoner basert på diverse foreldre og på utbetalt_lonn.
# # I tilegg til en knapp for å bekrefte utbetalelse før hele systemet er på plass.
#     """
#     Oversikt over hvem(PersonellRolle) som jobbet på hvilken aktivitet på en spesifikk dato(AktivitetDatoer).
    
#     Planlagt brukt i flere tabeller forbi fase 1.
#     """
#     aktivitet_datoer = models.ForeignKey(AktivitetDatoer, on_delete=models.PROTECT)
#     personel_rolle = models.ForeignKey(PersonellRolle, on_delete=models.PROTECT)
#     utbetalt_lonn = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.personel_rolle} {self.aktivitet_datoer} - Status utbetaling: {self.utbetalt_lonn}"

#     class Meta:
#         verbose_name = "Personell oppmøte"
#         verbose_name_plural = "Personellinfo: Personell oppmøte"