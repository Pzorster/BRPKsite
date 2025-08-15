from django.core.validators import RegexValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from datetime import timedelta

kun_tall_validator = RegexValidator(r'^\d+$', 'Kun tillatt med tall. Fjern tomrom.')

# Unsolved collection:
# 1.General: Reformater etter standarder? En gang og så få AI til å hjelpe meg med å finne convensions feil.
# 2.General: Hvor trengs det mer valdiering?
# 3.General: Consider edge cases
# 4.PersonellRolle: Må generers automatisk for vikarer
# 5.Betalings klasser: flytte betalingsinfo før aktivitet(one to many)? Sånn at i MedlemPameldt så er betalingsinfo lagret der?


# Del 1: Aktiviteter og personell - Legges til internt

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
    # For øyeblikket løst med help_text. Endres i fremtiden dersom problematisk.
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


class MalgruppeAktivitet(models.Model):
    """
    Kobler en målgrupp vi har sammen med aktivitets nivået vi tilbyr de.
    
    Brukes av:
    Aktivitet - hvem som deltar på aktiviteten.


    Med erfaring kan denne formateringen revurderes å brytes opp på en annen måte.
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
        #Formatterer for å ikke vise årstallet ved visning.
        formattert_dato = self.dato.strftime('%d %b')
        return f"{formattert_dato} - {self.begrunnelse}"

    class Meta:
        ordering = ['dato']
        verbose_name = "Datoer som utgår"
        verbose_name_plural = "Aktivitetsinfo: Datoer som utgår"

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

class Personell(models.Model):

    """
    Har all informasjon om personer som gjør frivillig eller lønnet arbeid for foreningen.
    
    Brukes av:
    PersonellRolle - hvilken roller personen opptrer i.

    Brukes i andre ting i senere faser.
    """
    fornavn = models.CharField(max_length=100)
    etternavn = models.CharField(max_length=100)
    mail = models.EmailField(max_length=100)
    tlf = models.CharField(max_length=8, validators=[kun_tall_validator],)
    fodsels_dato = models.CharField(max_length=11, blank=True)
    konto_nummer = models.CharField(max_length=20, validators=[kun_tall_validator])
    adresse = models.CharField(max_length=100)
    post_nummer = models.CharField(max_length=4, validators=[kun_tall_validator])
    skatt_info = models.TextField(verbose_name= "Hva trenger vi å vite om dine skatteforhold for å betale ut lønn?")
    annen_info = models.TextField(blank=True)

    def __str__(self):
        return f"{self.fornavn} {self.etternavn}"

    class Meta:
        verbose_name = "Personell"
        verbose_name_plural = "Personell"

class PersonellRolle(models.Model):
    """
    Har oversikt over hvilken roller forskjellige personer har.
    
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

class Aktivitet(models.Model):

# Filter/sorter på en del av attr.
# Ta en endelig vurdering på Choice formateringen du har lyst å kjøre.
    """
    All nødvendig informasjon om en spesifikk aktivitet. Diverse ForeignKeys.
    
    Brukes av:
    MedlemPameldt - Oversikt over hvilken medlemmer som går på hvilken aktivitet.
    AktivitetsDatoer - Oversikt over alle datoene en aktivitet går
    """
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
    
    # Regner ut ledige plasser for aktiviteteten
    @property
    def current_ledige_plasser(self):
        # Real-time calculation when accessed
        opptatte_plasser = self.pameldte_deltagere.count()
        return max(0, self.antall_plasser - opptatte_plasser)
    
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
    def display_price(self):
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

# Del 2: Medlemmer, deltagere og kundekontakt - lagt inn gjennom nettsiden


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

# Correct class name

class ForesporselKategori(models.Model):

# Skal dette endres fra kategori/beskrivelse til kategori/underkategeori eller kategori i seg selv være k/u eller skal __str__sette de sammen?
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

class KundeKontakt(models.Model):

# Trenger filter på kateogri, dato, fulgt_opp
# Trenger mail knapp som tar med seg info over i en mail
    """
    Forskjellige forespørsler(ForesporselKategori) som kommer inn via nettsiden og kontaktinformasjon til de som sender de inn.
    
    Planlagt bruk flere steder forbi fase 1.
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
        return f'{self.kategori} - {self.dato}'

    class Meta:
        verbose_name = "Forspørsel"
        verbose_name_plural = "Forspørsler"


# Del 3: Tabeller satt sammen av andre tabeller

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
# Forbi en viss fase legg inn statistikk funksjoner

class Bilde(models.Model):
    """
    Bilder som kan vises på siden.
    """
    bilde = models.ImageField(upload_to='images/')
    alternativ_tekst = models.CharField(max_length=100)
    rekkefolge = models.IntegerField()
    # Set up logic on admin side to both cut the picture to the right size and to make sure it gets a unique order
    # Probably easier to just tell people that it needs to be a certain size and parameters for them to upload it....
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

class GenerellKursInfo(models.Model):
    """
    Generell informasjon brukere får før påmelding.
    """
    informasjon = models.JSONField()
    i_bruk = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Informasjon om kursene"
        verbose_name_plural = "Informasjon om kursene"
