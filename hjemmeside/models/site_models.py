from django.db import models
from .validators import *


class ForesporselKategori(models.Model):
    """
    Kategorier som personer kan velge når de sender inn forespørsler gjennom nettsiden.
    
    Brukes av:
    KundeKontakt - For å kategorisere forespørsler.
    """
    kategori = models.CharField(max_length = 30)
    beskrivelse = models.TextField()

    def __str__(self):
        return self.kategori
    
    class Meta:
        verbose_name = "Kategori for forespørsler"
        verbose_name_plural = "Forespørselinfo: Kategorier"


# Future 1: Ønsker mail knapp som tar med seg info over i en mail
# Future 2: Directly integrated into the site mail
class KundeKontakt(models.Model):
    """
    Forskjellige forespørsler(ForesporselKategori) som kommer inn via nettsiden og kontaktinformasjon til de som sender de inn.
    
    Svares på av admin via Gmail.
    """

    status = (
        ('Motatt', 'Motatt'),
        ('Pågående', 'Pågående'),
        ('Ferdig', 'Ferdig')
    )
    navn = models.CharField(max_length = 30)
    mail = models.EmailField(max_length = 100)
    tlf = models.CharField(max_length = 8,  validators = [kun_tall_validator])
    kategori = models.ForeignKey(ForesporselKategori, on_delete = models.PROTECT)
    detaljer = models.TextField()
    dato = models.DateField(auto_now_add = True)
    fulgt_opp = models.CharField(max_length=10, choices=status, default='Motatt')

    def __str__(self):
        return f'{self.kategori} - {self.dato} - {self.fulgt_opp}'

    class Meta:
        verbose_name = "Forspørsel"
        verbose_name_plural = "Forspørsler"

# Future 1: A function to crop the pictures you upload to the site
# Future 2: Slider to determine the speed of the sldieshow on the page
class Bilde(models.Model):

    # Current 1: Info text so people know what ratio/size the pictures have to currently be to work with the site.

    """
    Bilder som kan vises på siden.
    """
    bilde = models.ImageField(upload_to='images/')
    alternativ_tekst = models.CharField(max_length=100)
    rekkefolge = models.IntegerField()
    i_bruk = models.BooleanField(default=True)

    def __str__(self):
        return self.alternativ_tekst

    class Meta:
        verbose_name = "Bilde"
        verbose_name_plural = "Bilder"
        ordering = ['rekkefolge']

class ForeningInfo(models.Model):
    """
    Informasjon om foreningen som vises på siden. Skal samstemme med det som er regisrert i brreg.no.
    """

    organisasjon_navn = models.CharField(max_length=40, default="Bergen Parkour")
    adresse = models.CharField(max_length=100)
    post_nummer = models.CharField(max_length=40)
    organisasjon_nummer = models.CharField(max_length=9, validators=[kun_tall_validator], default="923132228")
    kontakt_tlf = models.CharField(max_length=8, validators=[kun_tall_validator])
    kontakt_mail = models.CharField(max_length=40, default="bergen.parkour@gmail.com")
    facebook_side = models.CharField(max_length=20, default="Bergenparkour")
    instagram_side = models.CharField(max_length=20, default="bergenparkour")
    om_foreningen = models.TextField()
    i_bruk = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Informasjon om foreningen"
        verbose_name_plural = "Informasjon om foreningen"

