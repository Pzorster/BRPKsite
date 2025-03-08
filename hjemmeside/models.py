from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db import models

kun_tall_validator = RegexValidator(r'^\d+$', 'Kun tillatt med tall. Fjern tomrom.')


# Del 1: Aktiviteter og personell - Internally added

# Sub 1: Parents - Course details

class TypeAktivitet(models.Model):
    type_aktivitet = models.CharField(max_length=40)

    def __str__(self):
        return self.type_aktivitet

    class Meta:
        verbose_name = "Type aktivitet"
        verbose_name_plural = "Type aktivtet"

class StedAktivitet(models.Model):
    omrade = models.CharField(max_length=40)
    oppmote_sted = models.TextField()
    # Test hvordan JSONField funker og så kanskje sett inn en validator her og
    samarbeids_partnere = models.JSONField(blank=True, default=list)

    def __str__(self):
        return self.omrade

    class Meta:
        verbose_name = "Sted for aktivitet"
        verbose_name_plural = "Sted for aktivitet"

class MalgruppeAktivitet(models.Model):
    alder_eller_klasse = models.CharField(max_length=20, verbose_name="Alder/Kl")
    vanskelighetsgrad_eller_formål = models.CharField(max_length=20, verbose_name="Vanskelighetsgrad/Formål")

    def __str__(self):
        return self.alder_eller_klasse + " - " + self.vanskelighetsgrad_eller_formål

    class Meta:
        verbose_name = "Målgruppe for aktivitet"
        verbose_name_plural = "Målgruppe for aktivitet"

class DatoerSomUtgar(models.Model):
    dato = models.DateField()
    begrunnelse = models.CharField(max_length=100)

    def __str__(self):
        return str(self.dato) + " " + self.begrunnelse

    class Meta:
        verbose_name = "Datoer som utgår"
        verbose_name_plural = "Datoer som utgår"

# Sub 2: Parent - Personell details

class Personell(models.Model):
    fornavn = models.CharField(max_length=100)
    etternavn = models.CharField(max_length=100)
    mail = models.EmailField(max_length=100)
    tlf = models.CharField(max_length=8, validators=[kun_tall_validator],)
    # Reconsider how you store personnummer due to security issues
    person_nummer = models.CharField(max_length=11)
    konto_nummer = models.CharField(max_length=20, validators=[kun_tall_validator])
    adresse = models.CharField(max_length=100)
    post_nummer = models.CharField(max_length=4, validators=[kun_tall_validator])
    skatt_info = models.TextField(verbose_name= "Hva trenger vi å vite om dine skatteforhold for å betale ut lønn?")
    annen_info = models.TextField(blank=True)

    def __str__(self):
        return self.fornavn + " " + self.etternavn

    class Meta:
        verbose_name = "Personell"
        verbose_name_plural = "Personell"

class Rolle(models.Model):
    rolle = models.CharField(max_length=20)
    lonn = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.rolle}"

    class Meta:
        verbose_name = "Rolle"
        verbose_name_plural = "Roller"

class AktivitetPersonell(models.Model):
    aktivitet = models.ForeignKey("Aktivitet", on_delete=models.CASCADE)
    personell = models.ForeignKey(Personell, on_delete=models.CASCADE)
    rolle = models.ForeignKey(Rolle, on_delete = models.PROTECT)

    def __str__(self):
        return f"{self.personell} {self.rolle}"

    class Meta:
        verbose_name = "Hvem/Hvor/Hvilken Rolle"
        verbose_name_plural = "Hvem/Hvor/Hvilken Rolle"

# Main

class Aktivitet(models.Model):
    type_aktivitet = models.ForeignKey(TypeAktivitet, on_delete=models.PROTECT)
    sted = models.ForeignKey(StedAktivitet, on_delete=models.PROTECT)
    malgruppe = models.ForeignKey(MalgruppeAktivitet, on_delete=models.PROTECT)
    oppstart = models.DateField()
    slutt = models.DateField()
    kl_start = models.TimeField()
    kl_slutt = models.TimeField()
    antall_ganger = models.PositiveIntegerField()
    pris = models.PositiveIntegerField()
    # ansvars_personer = models.ManyToManyField(Personell)
    ansvars_personer = models.ManyToManyField(Personell, through='AktivitetPersonell')
    datoer_som_utgar = models.ManyToManyField(DatoerSomUtgar)

    def __str__(self):
        return str(self.sted) + " " + str(self.malgruppe)

    class Meta:
        verbose_name = "Aktivitet"
        verbose_name_plural = "Aktiviteter"


# Del 2: Medlemmer og deltagere - Added mainly through frontend forms

class Medlem(models.Model):
    roller = (
        ('Deltager/medlem', 'Deltager/medlem'),
        ('Far', 'Far'),
        ('Mor', 'Mor'),
        ('Verge', 'Verge'),
        ('Annen Familie', 'Annen Familie')
    )

    fornavn = models.CharField(max_length = 30)
    etternavn = models.CharField(max_length = 30)
    alder = models.PositiveIntegerField()
    fodt_ar = models.PositiveIntegerField()
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
    pameldt = models.ManyToManyField(Aktivitet, blank=True)
    # Notater is for internal stuff and should not be shown externally
    notater = models.TextField(blank=True)
    

    def clean(self):
        for i in range(2, 4):  # Loop for kontakt2 and kontakt3
            tlf = getattr(self, f'kontakt{i}_tlf')
            mail = getattr(self, f'kontakt{i}_mail')
            rolle = getattr(self, f'kontakt{i}_rolle')

            if tlf and (not mail or not rolle):
                raise ValidationError({f'kontakt{i}_mail': 'Hvis telefon er fylt ut, må e-post og rolle også fylles ut.'})
            if mail and (not tlf or not rolle):
                raise ValidationError({f'kontakt{i}_tlf': 'Hvis e-post er fylt ut, må telefon og rolle også fylles ut.'})
            if rolle and (not tlf or not mail):
                raise ValidationError({f'kontakt{i}_tlf': 'Hvis rolle er valgt, må telefon og e-post også fylles ut.'})

    def save(self, *args, **kwargs):
        self.clean()  # Ensure clean() runs before saving
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Medlem"
        verbose_name_plural = "Medlemmer"


class MeldtInteresse(models.Model):
    mail = models.EmailField(max_length = 100)
    tlf = models.CharField(max_length = 8,  validators = [kun_tall_validator])
    oppsummert = models.CharField(max_length = 100)
    detaljer = models.TextField()
    dato = models.DateField(auto_now_add = True)
    fulgt_opp = models.BooleanField(default = False)

    def __str__(self):
        return f'{self.oppsumert} - {self.dato}'

    class Meta:
        verbose_name = "Meldt interesse for aktivitet"
        verbose_name_plural = "Meldt interesse for aktivitet"

class KontakterForening(models.Model):
    mail = models.EmailField(max_length = 100)
    tlf = models.CharField(max_length = 8,  validators = [kun_tall_validator])
    oppsummert = models.CharField(max_length = 100)
    detaljer = models.TextField()
    dato = models.DateField(auto_now_add = True)
    fulgt_opp = models.BooleanField(default = False)

    def __str__(self):
        return f'{self.oppsumert} - {self.dato}'

    class Meta:
        verbose_name = "Forespørsler til forenigen"
        verbose_name_plural = "Forespørsler til forenigen"



# Del 3: Undervisnings tabeller - brukes av instruktører

class Oppmote(models.Model):
    aktivitet = models.ForeignKey(Aktivitet, on_delete = models.PROTECT)
    medlem = models.ForeignKey(Medlem, on_delete = models.PROTECT)

    # For øyeblikket er de hardcoded for max 20 ganger, som pleier å være maks på 1 semester
    tilstede_1 = models.BooleanField(default = False)
    tilstede2 = models.BooleanField(default = False)
    tilstede3 = models.BooleanField(default = False)
    tilstede4 = models.BooleanField(default = False)
    tilstede5 = models.BooleanField(default = False)
    tilstede6 = models.BooleanField(default = False)
    tilstede7 = models.BooleanField(default = False)
    tilstede8 = models.BooleanField(default = False)
    tilstede9 = models.BooleanField(default = False)
    tilstede10 = models.BooleanField(default = False)
    tilstede11 = models.BooleanField(default = False)
    tilstede12 = models.BooleanField(default = False)
    tilstede13 = models.BooleanField(default = False)
    tilstede14 = models.BooleanField(default = False)
    tilstede15 = models.BooleanField(default = False)
    tilstede16 = models.BooleanField(default = False)
    tilstede17 = models.BooleanField(default = False)
    tilstede18 = models.BooleanField(default = False)
    tilstede19 = models.BooleanField(default = False)
    tilstede20 = models.BooleanField(default = False)

    class Meta:
        unique_together = ('aktivitet', 'medlem')
        verbose_name = "Oppmøte lister"
        verbose_name_plural = "Oppmøte lister"

    def clean(self):
        max_ganger = self.aktivitet.antall_ganger
        for i in range (max_ganger + 1, 21):
            setattr(self, f'tilstede{i}', False)

    def __str__(self):
        return f"Oppmøte på {self.aktivitet}"

class KontaktListe(models.Model):
    aktivitet = models.ForeignKey(Aktivitet, on_delete=models.PROTECT)
    medlem = models.ForeignKey(Medlem, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('aktivitet', 'medlem')  # Prevent duplicates
        verbose_name = "Kontakt lister"
        verbose_name_plural = "Kontakt lister"

    def get_hoved_kontakt_tlf(self):
        return self.medlem.hoved_kontakt_tlf  # Fetch dynamically

    def get_hoved_kontakt_rolle(self):
        return self.medlem.hoved_kontakt_rolle

    def get_foto_tillatelse(self):
        return self.medlem.foto_tillatelse

    def get_annet(self):
        return self.medlem.annet

    get_hoved_kontakt_tlf.short_description = "Hovedkontakt Tlf"
    get_hoved_kontakt_rolle.short_description = "Hovedkontakt Rolle"  # Admin column title
    get_foto_tillatelse.short_description = "Fototillatelse"
    get_annet.short_description = "Annen info"
    
    def __str__(self):
        return f"Kontaktinfo til {self.medlem}"

# End 4/3:  I've done what I will in the db, now I need to get it working admin side.

class TimeListePersonell(models.Model):
    personell = models.ForeignKey(Personell, on_delete = models.PROTECT)
    aktivitet = models.ForeignKey(Aktivitet, on_delete = models.PROTECT)
    dato_gjennomført = models.DateField()

    class Meta:
        unique_together = ('personell', 'aktivitet', 'dato_gjennomført')
        verbose_name = "Timeliste for personell"
        verbose_name_plural = "Timeliste for personell"

    def __str__(self):
        return f'{self.personell} jobbet på {self.aktivitet} den {self.dato_gjennomført}'


# Del 4: Økonomi tabeller - brukes av økonomisk ansvarlig

# Im waiting with this because I will be getting a lot of info from a lot of places and I dont know how
# the apis might be connecting

# Deltagere og betalinger
# Attr: medlem, aktivitet, aktivitet.pris, noen prisreduskjoner, når betaling ble gjennomført, hvor betalt: dnb, vipps, kontant

# Kontrakt info - goes out to a contract you can send - with checkboxes for what is already sent out

# Ansatte og utbetalt/opptjent lønn - goes out to lønnslipper - with checkboxes for utbetalt lønn
# Maybe fields are opptjent i periode, skattet, utbetalt, rabattert(when we don't have enough to run full pay)

