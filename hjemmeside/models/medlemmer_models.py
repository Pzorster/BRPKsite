from django.core.validators import RegexValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from datetime import timedelta
from .validators import *

class Medlem(models.Model):

# Trenger et filter for diverse
    """
    Informasjon om personer som melder seg inn i foreningen.
    
    Brukes av:
    MedlemPameldt - Oversikt over hvilken aktiviteter medlemmer er pameldt.
    Funksjon - Kontaktinfo til personell for aktiviteter
    """

# Skal formateringen på valgene endres?
    roller = (
        ('Deltager/medlem', 'Deltager/medlem'),
        ('Far', 'Far'),
        ('Mor', 'Mor'),
        ('Verge', 'Verge'),
        ('Annen Familie', 'Annen Familie')
    )

    fornavn = models.CharField(max_length = 30)
    etternavn = models.CharField(max_length = 30)
    fodt_ar = models.DateField()
    alder = models.PositiveIntegerField(editable=False)
    adresse = models.CharField(max_length = 100)
    post_nummer = models.CharField(max_length=4, validators=[kun_tall_validator])
    foto_tillatelse = models.BooleanField(choices = [(True, "Ja"), (False, "Nei")])
    hoved_kontakt_tlf = models.CharField(max_length = 8, validators = [kun_tall_validator])
    hoved_kontakt_mail = models.EmailField(max_length = 100)
    hoved_kontakt_rolle = models.CharField(max_length=20, choices=roller)
    kontakt2_tlf = models.CharField(max_length = 8, validators = [kun_tall_validator], blank=True)
    kontakt2_mail = models.EmailField(max_length = 100, blank=True)
    kontakt2_rolle = models.CharField(max_length=20, choices=roller, blank=True)
    kontakt3_tlf = models.CharField(max_length = 8, validators = [kun_tall_validator], blank=True)
    kontakt3_mail = models.EmailField(max_length = 100, blank=True)
    kontakt3_rolle = models.CharField(max_length=20, choices=roller, blank=True)
    annet = models.TextField(blank=True)
    # Notater is for internal stuff and should not be shown externally
    notater = models.TextField(blank=True)

    def __str__(self):
        return self.fornavn + " " + self.etternavn
    

    def clean(self):

        # Validerer når folk fyller inn kontakt2 og kontakt3
        for i in range(2, 4):
            tlf = getattr(self, f'kontakt{i}_tlf')
            mail = getattr(self, f'kontakt{i}_mail')
            rolle = getattr(self, f'kontakt{i}_rolle')

            if tlf and (not mail or not rolle):
                raise ValidationError({f'kontakt{i}_mail': 'Hvis telefon er fylt ut, må e-post og rolle også fylles ut.'})
            if mail and (not tlf or not rolle):
                raise ValidationError({f'kontakt{i}_tlf': 'Hvis e-post er fylt ut, må telefon og rolle også fylles ut.'})
            if rolle and (not tlf or not mail):
                raise ValidationError({f'kontakt{i}_tlf': 'Hvis rolle er valgt, må telefon og e-post også fylles ut.'})

    # Brukes for å periodisk omregne alder på deltagere
    @property
    def current_age(self):
        today = timezone.now().date()
        born = self.fodt_ar
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    

    def save(self, *args, **kwargs):

# Er dette ved registrering eller ved alle endringer?
        # Regner ut alder på person
        today = timezone.now().date()
        born = self.fodt_ar
        self.alder = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

        # Kjører valdieringen før lagring
        self.clean()  
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Medlem"
        verbose_name_plural = "Medlemmer"