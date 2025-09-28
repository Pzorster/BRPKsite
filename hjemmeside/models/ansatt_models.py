from django.db import models
from .validators import kun_tall_validator


class Rolle(models.Model):
    """
    Definerer forskjellige roller en person kan ha i foreningen. Både betalte og frivillige.
    
    Brukes av:
    PersonellRolle - I hvilken roller personell opptrer i.
    """
    rolle = models.CharField(max_length=20)
    standard_lonn = models.PositiveIntegerField()

    def __str__(self):
        return self.rolle

    class Meta:
        verbose_name = "Rolle"
        verbose_name_plural = "Personellinfo: Roller"

# Future 1: Will be used for paying out salary and recording payment history
class Personell(models.Model):
    """
    Har all informasjon om personer som gjør frivillig eller lønnet arbeid for foreningen.
    
    Brukes av:
    PersonellRolle - hvilken roller personen opptrer i.
    """
    fornavn = models.CharField(max_length=100)
    etternavn = models.CharField(max_length=100)
    mail = models.EmailField(max_length=100)
    tlf = models.CharField(max_length=8, validators=[kun_tall_validator],)
    fodsels_dato = models.CharField(max_length=6, validators=[kun_tall_validator], blank=True)
    konto_nummer = models.CharField(max_length=20, validators=[kun_tall_validator])
    adresse = models.CharField(max_length=100)
    post_nummer = models.CharField(max_length=4, validators=[kun_tall_validator])
    skatt_info = models.TextField(verbose_name= "Hva trenger vi å vite om dine skatteforhold for å betale ut lønn? Type informasjon om skattekort/frikort.")
    annen_info = models.TextField(blank=True)

    def __str__(self):
        return f"{self.fornavn} {self.etternavn}"

    class Meta:
        verbose_name = "Personell"
        verbose_name_plural = "Personell"

# Future 1: Will be used for calculating salary
class PersonellRolle(models.Model):
    """
    Oversikt over hvilken roller forskjellige personer har.
    
    Brukes av:
    Aktivitet - hvilken person de har i hvilken rolle.
    """
    rolle = models.ForeignKey(Rolle, on_delete=models.PROTECT)
    personell = models.ForeignKey(Personell, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.personell} {self.rolle}"
    
    class Meta:
        verbose_name = "Personell i rollen som"
        verbose_name_plural = "Personellinfo: Personell i rollen som"
