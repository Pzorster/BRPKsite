from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, time, timedelta
from random import choice, randint, random, sample

from hjemmeside.models import *

class Command(BaseCommand):
    """
    A command that generates test data for the database and website.
    """
    help = "Creates DB data for testing"

    def handle(self, *args, **kwargs):
        # Ensure superuser exists
        user = User.objects.filter(username = "admin", is_superuser = True)
        if not user.exists():
            user = User.objects.create_superuser(username = "admin", password = "test")
        
        self.stdout.write("Creating test data...")
        
        # Create base data for all models
        self.create_type_aktivitet()
        self.create_sted_aktivitet()
        self.create_malgruppe_aktivitet()
        self.create_datoer_som_utgar()
        self.create_roller()
        self.create_personell()
        self.create_personell_roller()
        self.create_aktiviteter()
        self.create_medlemmer()
        self.create_foresporsel_kategorier()
        self.create_kunde_kontakt()
        self.create_medlem_pameldt()
        self.create_betalings_type()
        self.create_betaling_status()
        self.create_deltager_oppmote()
        self.create_personell_oppmote()
        self.create_betaling_status_drop_in()
        
        self.stdout.write(self.style.SUCCESS("Test data created successfully!"))
        
    def create_type_aktivitet(self):
        self.stdout.write("Creating TypeAktivitet...")
        aktivitets_typer = [
            {"type_aktivitet": "Semesterkurs"},
            {"type_aktivitet": "Feriekurs"},
            {"type_aktivitet": "Jam"},
            {"type_aktivitet": "Samling"}
        ]

        self.type_liste = []
        for i in aktivitets_typer:
            self.type_liste.append(TypeAktivitet.objects.create(**i))
        
    def create_sted_aktivitet(self):
        self.stdout.write("Creating StedAktivitet...")
        aktivitets_steder = [
            {"omrade": "Nesttun", "oppmote_sted": "Foran Fana Kulturhus"},
            {"omrade": "Olsvik", "oppmote_sted": "Olsvik parkour park"},
            {"omrade": "Åsane", "oppmote_sted": "Fysak Åsane 2.etg"},
            {"omrade": "Bergen Sentrum", "oppmote_sted": "Etter beskjed"},
        ]

        self.steder_liste = []
        for i in aktivitets_steder:
            self.steder_liste.append(StedAktivitet.objects.create(**i))

    def create_malgruppe_aktivitet(self):
        self.stdout.write("Creating MalgruppeAktivitet...")
        aktivitets_malgruppe = [
            {"alder_eller_klasse": "1-3.kl", "vanskelighetsgrad_eller_formal": "Blandet"},
            {"alder_eller_klasse": "4-7.kl", "vanskelighetsgrad_eller_formal": "Blandet"},
            {"alder_eller_klasse": "8.kl+", "vanskelighetsgrad_eller_formal": "Blandet"},
            {"alder_eller_klasse": "5-7.kl", "vanskelighetsgrad_eller_formal": "Viderekomen"},
            {"alder_eller_klasse": "5-10.kl", "vanskelighetsgrad_eller_formal": "Teknisk"},
            {"alder_eller_klasse": "1.vgs+", "vanskelighetsgrad_eller_formal": "Teknisk"},
            {"alder_eller_klasse": "Voksne", "vanskelighetsgrad_eller_formal": "Blandet"}
        ]

        self.malgruppe_liste = []
        for i in aktivitets_malgruppe:
            self.malgruppe_liste.append(MalgruppeAktivitet.objects.create(**i))

    def create_datoer_som_utgar(self):
        self.stdout.write("Creating DatoerSomUtgar...")
        datoer_som_utgar = [
            {"dato": date(2025, 2, 27), "begrunnelse": "Vinterferie"},
            {"dato": date(2025, 4, 14), "begrunnelse": "Påske"},
            {"dato": date(2025, 4, 15), "begrunnelse": "Påske"},
            {"dato": date(2025, 4, 16), "begrunnelse": "Påske"},
            {"dato": date(2025, 4, 17), "begrunnelse": "Påske"},
            {"dato": date(2025, 4, 18), "begrunnelse": "Påske"},
            {"dato": date(2025, 4, 21), "begrunnelse": "Påske"},
            {"dato": date(2025, 5, 1), "begrunnelse": "Helligdag"},
            {"dato": date(2025, 5, 2), "begrunnelse": "Planleggingsdag"},
            {"dato": date(2025, 5, 29), "begrunnelse": "Helligdag"},
            {"dato": date(2025, 5, 30), "begrunnelse": "Planleggingsdag"},
        ]

        self.datoer_liste = []
        for i in datoer_som_utgar:
            self.datoer_liste.append(DatoerSomUtgar.objects.create(**i))

    def create_roller(self):
        self.stdout.write("Creating Rolle...")
        roller = [
            {"rolle": "Instruktør", "standard_lonn": 300},
            {"rolle": "Assistent", "standard_lonn": 250},
            {"rolle": "Ansvarlig", "standard_lonn": 300},
            {"rolle": "Hovedinstruktør", "standard_lonn": 650},
            {"rolle": "Frivillig", "standard_lonn": 0}
        ]

        self.rolle_liste = []
        for i in roller:
            self.rolle_liste.append(Rolle.objects.create(**i))

    def create_personell(self):
        self.stdout.write("Creating Personell...")
        personell = [
            {"fornavn": "Peter", "etternavn": "Johnsen", "mail": "pj@mail.no", "tlf": "92929292", "konto_nummer": "32323232323", "adresse": "Morsom 1", "post_nummer": "3421", "skatt_info": "Frikort. BRPK eneste arbeidsgiver"},
            {"fornavn": "Ole", "etternavn": "Grønn", "mail": "pj@mail.no", "tlf": "92929292", "konto_nummer": "32323232323", "adresse": "Morsom 1", "post_nummer": "3421", "skatt_info": "Frikort. BRPK eneste arbeidsgiver"},
            {"fornavn": "Johanne", "etternavn": "Petersen", "mail": "pj@mail.no", "tlf": "92929292", "konto_nummer": "32323232323", "adresse": "Morsom 1", "post_nummer": "3421", "skatt_info": "Frikort. BRPK eneste arbeidsgiver"},
            {"fornavn": "Siri", "etternavn": "Rød", "mail": "pj@mail.no", "tlf": "92929292", "konto_nummer": "32323232323", "adresse": "Morsom 1", "post_nummer": "3421", "skatt_info": "Frikort. BRPK eneste arbeidsgiver"},
            {"fornavn": "Olav", "etternavn": "Trygve", "mail": "pj@mail.no", "tlf": "92929292", "konto_nummer": "32323232323", "adresse": "Morsom 1", "post_nummer": "3421", "skatt_info": "Frikort. BRPK eneste arbeidsgiver"},
            {"fornavn": "Jorunn", "etternavn": "Mentra", "mail": "pj@mail.no", "tlf": "92929292", "konto_nummer": "32323232323", "adresse": "Morsom 1", "post_nummer": "3421", "skatt_info": "Frikort. BRPK eneste arbeidsgiver"},
            {"fornavn": "Thor", "etternavn": "Trond", "mail": "pj@mail.no", "tlf": "92929292", "konto_nummer": "32323232323", "adresse": "Morsom 1", "post_nummer": "3421", "skatt_info": "Frikort. BRPK eneste arbeidsgiver"},
            {"fornavn": "Selje", "etternavn": "Orden", "mail": "pj@mail.no", "tlf": "92929292", "konto_nummer": "32323232323", "adresse": "Morsom 1", "post_nummer": "3421", "skatt_info": "Frikort. BRPK eneste arbeidsgiver"},
        ]

        self.personell_liste = []
        for i in personell:
            self.personell_liste.append(Personell.objects.create(**i))

    def create_personell_roller(self):
        self.stdout.write("Creating PersonellRolle...")
        self.personell_rolle_liste = []
        
        for i in range(len(self.personell_liste)):
            # Assign 1-2 random roles to each personnel
            for _ in range(randint(1, 2)):
                rolle = choice(self.rolle_liste)
                personell_rolle = PersonellRolle.objects.create(
                    rolle=rolle,
                    personell=self.personell_liste[i]
                )
                self.personell_rolle_liste.append(personell_rolle)

    def create_aktiviteter(self):
        self.stdout.write("Creating Aktivitet...")
        aktiviteter = [
            {"type_aktivitet_index": 0, "sted_index": 0, "malgruppe_index": 0, "start_dato": date(2025, 3, 3),
            "kl_start": time(17), "kl_slutt": time(18), "antall_ganger": 12, "antall_plasser": 15, 
            "pris_vanlig": 1300, "pris_drop_in": 150, "dag_interval": 7, "datoer_som_utgar_indexes": [1,6]},
            {"type_aktivitet_index": 0, "sted_index": 0, "malgruppe_index": 1, "start_dato": date(2025, 3, 3),
            "kl_start": time(18), "kl_slutt": time(19), "antall_ganger": 12, "antall_plasser": 15, 
            "pris_vanlig": 1300, "pris_drop_in": 150, "dag_interval": 7, "datoer_som_utgar_indexes": [1,6]},
            {"type_aktivitet_index": 0, "sted_index": 0, "malgruppe_index": 3, "start_dato": date(2025, 3, 3),
            "kl_start": time(19), "kl_slutt": time(20), "antall_ganger": 12, "antall_plasser": 15, 
            "pris_vanlig": 1300, "pris_drop_in": 150, "dag_interval": 7, "datoer_som_utgar_indexes": [1,6]},
            {"type_aktivitet_index": 0, "sted_index": 0, "malgruppe_index": 2, "start_dato": date(2025, 3, 3),
            "kl_start": time(20), "kl_slutt": time(21), "antall_ganger": 12, "antall_plasser": 15, 
            "pris_vanlig": 1300, "pris_drop_in": 150, "dag_interval": 7, "datoer_som_utgar_indexes": [1,6]},
            {"type_aktivitet_index": 0, "sted_index": 1, "malgruppe_index": 0, "start_dato": date(2025, 3, 4),
            "kl_start": time(17), "kl_slutt": time(18), "antall_ganger": 12, "antall_plasser": 15, 
            "pris_vanlig": 0, "pris_drop_in": 0, "dag_interval": 7, "datoer_som_utgar_indexes": [2]},
            {"type_aktivitet_index": 0, "sted_index": 1, "malgruppe_index": 1, "start_dato": date(2025, 3, 4),
            "kl_start": time(18), "kl_slutt": time(19), "antall_ganger": 12, "antall_plasser": 15, 
            "pris_vanlig": 0, "pris_drop_in": 0, "dag_interval": 7, "datoer_som_utgar_indexes": [2]},
            {"type_aktivitet_index": 0, "sted_index": 1, "malgruppe_index": 3, "start_dato": date(2025, 3, 4),
            "kl_start": time(19), "kl_slutt": time(20), "antall_ganger": 12, "antall_plasser": 15, 
            "pris_vanlig": 0, "pris_drop_in": 0, "dag_interval": 7, "datoer_som_utgar_indexes": [2]},
            {"type_aktivitet_index": 0, "sted_index": 2, "malgruppe_index": 0, "start_dato": date(2025, 3, 5),
            "kl_start": time(17), "kl_slutt": time(18), "antall_ganger": 13, "antall_plasser": 15, 
            "pris_vanlig": 1400, "pris_drop_in": 150, "dag_interval": 7, "datoer_som_utgar_indexes": [3]},
            {"type_aktivitet_index": 0, "sted_index": 2, "malgruppe_index": 1, "start_dato": date(2025, 3, 5),
            "kl_start": time(18), "kl_slutt": time(19), "antall_ganger": 13, "antall_plasser": 15, 
            "pris_vanlig": 1400, "pris_drop_in": 150, "dag_interval": 7, "datoer_som_utgar_indexes": [3]},
            {"type_aktivitet_index": 0, "sted_index": 2, "malgruppe_index": 2, "start_dato": date(2025, 3, 5),
            "kl_start": time(19), "kl_slutt": time(20), "antall_ganger": 13, "antall_plasser": 15, 
            "pris_vanlig": 1400, "pris_drop_in": 150, "dag_interval": 7, "datoer_som_utgar_indexes": [3]},
            {"type_aktivitet_index": 0, "sted_index": 3, "malgruppe_index": 4, "start_dato": date(2025, 1, 23),
            "kl_start": time(16, 30), "kl_slutt": time(18), "antall_ganger": 16, "antall_plasser": 15, 
            "pris_vanlig": 1750, "pris_drop_in": 175, "dag_interval": 7, "datoer_som_utgar_indexes": [0,4,7,9]},
            {"type_aktivitet_index": 0, "sted_index": 3, "malgruppe_index": 5, "start_dato": date(2025, 1, 23),
            "kl_start": time(18, 30), "kl_slutt": time(20), "antall_ganger": 16, "antall_plasser": 15, 
            "pris_vanlig": 1750, "pris_drop_in": 175, "dag_interval": 7, "datoer_som_utgar_indexes": [0,4,7,9]},
            {"type_aktivitet_index": 0, "sted_index": 3, "malgruppe_index": 6, "start_dato": date(2025, 1, 24),
            "kl_start": time(18), "kl_slutt": time(19, 30), "antall_ganger": 12, "antall_plasser": 15, 
            "pris_vanlig": 1300, "pris_drop_in": 150, "dag_interval": 7, "datoer_som_utgar_indexes": [5,8,10]},
        ]

        self.aktivitet_liste = []
        for a in aktiviteter:
            # Create base aktivitet
            aktivitet = Aktivitet(
                type_aktivitet=self.type_liste[a["type_aktivitet_index"]],
                sted=self.steder_liste[a["sted_index"]],
                malgruppe=self.malgruppe_liste[a["malgruppe_index"]],
                start_dato=a["start_dato"],
                kl_start=a["kl_start"],
                kl_slutt=a["kl_slutt"],
                antall_ganger=a["antall_ganger"],
                antall_plasser=a["antall_plasser"],
                ledige_plasser=a["antall_plasser"],
                pris_vanlig=a["pris_vanlig"],
                pris_drop_in=a["pris_drop_in"],
                dag_interval=a["dag_interval"]
            )
            aktivitet.save()  # First save to get PK
            
            # Assign excluded dates
            datoer_indexes = a["datoer_som_utgar_indexes"]
            if isinstance(datoer_indexes, list):
                datoer = [self.datoer_liste[i] for i in datoer_indexes]
            else:
                datoer = [self.datoer_liste[datoer_indexes]]
                
            aktivitet.datoer_som_utgar.set(datoer)
            
            # Assign 2-3 random staff to each activity
            random_personell = sample(self.personell_rolle_liste, min(randint(2, 3), len(self.personell_rolle_liste)))
            aktivitet.personell_rolle.set(random_personell)
            
            self.aktivitet_liste.append(aktivitet)


    def create_medlemmer(self):
        self.stdout.write("Creating Medlemmer...")
        
        # Data pools
        addresses = ["Parkveien 1", "Hovedgaten 45", "Lillebakken 12", "Strandveien 78", "Sentrum 9", "Bakkeveien 22"]
        post_numbers = ["5000", "5010", "5020", "5030", "5040", "5050"]
        emails = ["kontakt1@mail.com", "kontakt2@mail.com", "kontakt3@mail.com", "kontakt4@mail.com", "hjelp@mail.com"]
        first_names = ["Anna", "Bjørn", "Clara", "Daniel", "Emil", "Frida", "Gunnar", "Hanna", "Ivar", "Jenny"]
        last_names = ["Hansen", "Olsen", "Nilsen", "Johansen", "Larsen", "Andersen", "Pedersen", "Bakke"]
        kontakter_roller = ["Far", "Mor", "Verge", "Annen Familie"]

        age_map = {
            "1-3.kl": (6, 9),
            "4-7.kl": (10, 13),
            "8.kl+": (14, 17),
            "5-7.kl": (10, 13),
            "5-10.kl": (10, 16),
            "1.vgs+": (16, 19),
            "Voksne": (20, 40)
        }

        self.medlem_liste = []
        for _ in range(80):  # Create 80 members
            fornavn = choice(first_names)
            etternavn = choice(last_names)
            
            # Select an age group and generate appropriate age
            age_group = choice(list(age_map.keys()))
            age_range = age_map[age_group]
            alder = randint(age_range[0], age_range[1])
            
            # Calculate birth date (approximately)
            today = timezone.now().date()
            birth_year = today.year - alder
            birth_month = randint(1, 12)
            birth_day = randint(1, 28)  # Using 28 to be safe for all months
            fodt_ar = date(birth_year, birth_month, birth_day)
            
            medlem = Medlem(
                fornavn=fornavn,
                etternavn=etternavn,
                fodt_ar=fodt_ar,
                adresse=choice(addresses),
                post_nummer=choice(post_numbers),
                foto_tillatelse=choice([True, False]),
                hoved_kontakt_tlf=f"9{randint(1000000, 9999999)}",
                hoved_kontakt_mail=choice(emails),
                hoved_kontakt_rolle=choice(kontakter_roller),
                annet=choice(["", "Allergi: peanøtter", "Trenger ekstra oppfølging", ""])
            )
            
            # Add optional additional contacts
            for i in range(2, 4):
                if random() > 0.5:  # 50% chance of additional contact
                    setattr(medlem, f"kontakt{i}_tlf", f"9{randint(1000000, 9999999)}")
                    setattr(medlem, f"kontakt{i}_mail", choice(emails))
                    setattr(medlem, f"kontakt{i}_rolle", choice(kontakter_roller))
            
            medlem.save()  # Will calculate age automatically
            self.medlem_liste.append(medlem)

    def create_foresporsel_kategorier(self):
        self.stdout.write("Creating ForesporselKategori...")
        kategorier = [
            {"kategori": "Kurs", "beskrivelse": "Spørsmål om kurs"},
            {"kategori": "Medlemskap", "beskrivelse": "Spørsmål om medlemskap"},
            {"kategori": "Priser", "beskrivelse": "Spørsmål om priser"},
            {"kategori": "Timeplan", "beskrivelse": "Spørsmål om timeplan"},
            {"kategori": "Annet", "beskrivelse": "Andre spørsmål"}
        ]
        
        self.kategori_liste = []
        for k in kategorier:
            self.kategori_liste.append(ForesporselKategori.objects.create(**k))

    def create_kunde_kontakt(self):
        self.stdout.write("Creating KundeKontakt...")
        details = [
            "Jeg lurer på når neste kurs starter",
            "Kan jeg få informasjon om priser?",
            "Er det ledige plasser på kurset i Åsane?",
            "Hvordan melder jeg meg inn?",
            "Kan vi få et spesialtilbud for en gruppe?",
            "Har dere kurs for barn under skolealder?",
            "Jeg ønsker å bli instruktør, hvordan går jeg frem?"
        ]
        
        for _ in range(15):  # Create 15 inquiries
            KundeKontakt.objects.create(
                mail=f"kunde{randint(100, 999)}@mail.com",
                tlf=f"9{randint(1000000, 9999999)}",
                kategori=choice(self.kategori_liste),
                detaljer=choice(details),
                fulgt_opp=choice([True, False]),
            )
    
    def create_medlem_pameldt(self):
        self.stdout.write("Creating MedlemPameldt...")
        self.medlem_pameldt_liste = []
        
        for medlem in self.medlem_liste:
            # Determine how many activities this member joins (0-3)
            num_activities = min(randint(0, 3), len(self.aktivitet_liste))
            
            if num_activities > 0:
                # Select random activities without repetition
                aktiviteter = sample(self.aktivitet_liste, num_activities)
                
                for aktivitet in aktiviteter:
                    # 10% chance of being drop-in
                    drop_in = random() < 0.10
                    
                    medlem_pameldt = MedlemPameldt.objects.create(
                        aktivitet=aktivitet,
                        medlem=medlem,
                        drop_in=drop_in
                    )
                    self.medlem_pameldt_liste.append(medlem_pameldt)

    def create_betalings_type(self):
        self.stdout.write("Creating BetalingsType...")
        betalings_typer = [
            {"navn": "Bank"},
            {"navn": "Vipps"},
            {"navn": "Kontant"},
            {"navn": "Aktivitetskortet"},
            {"navn": "Tilskudd"}
        ]
        
        self.betalings_type_liste = []
        for bt in betalings_typer:
            self.betalings_type_liste.append(BetalingsType.objects.create(**bt))

    def create_betaling_status(self):
        self.stdout.write("Creating BetalingStatus...")
        
        # Create payment status for non-drop-in signups (about 80%)
        for mp in self.medlem_pameldt_liste:
            if not mp.drop_in:  # Only for regular signups, not drop-ins
                # 70% chance of having paid
                status_betaling = random() < 0.7
                
                # Random discount between 0-30%
                rabatt = round(random() * 0.3, 2) if random() < 0.3 else 0
                
                BetalingStatus.objects.create(
                    medlem_pameldt=mp,
                    type_betaling=choice(self.betalings_type_liste),
                    rabatt=rabatt,
                    status_betaling=status_betaling
                )

    def create_deltager_oppmote(self):
        self.stdout.write("Creating DeltagerOppmote...")
        
        # For each participant, create attendance records for activity dates
        for mp in self.medlem_pameldt_liste:
            # Get all dates for this activity
            aktivitet_datoer = mp.aktivitet.aktivitet_datoer.all()
            
            for dato in aktivitet_datoer:
                # If the date is in the past, record attendance (random)
                if dato.dato < timezone.now().date():
                    tilstede = random() < 0.8  # 80% attendance rate
                else:
                    tilstede = False
                
                DeltagerOppmote.objects.create(
                    aktivitet_datoer=dato,
                    medlem_pameldt=mp,
                    tilstede=tilstede
                )

    def create_personell_oppmote(self):
        self.stdout.write("Creating PersonellOppmote...")
        
        # For each activity, record staff attendance for past dates
        for aktivitet in self.aktivitet_liste:
            # Get personnel for this activity
            personell_roller = aktivitet.personell_rolle.all()
            
            # Get past dates for this activity
            past_dates = aktivitet.aktivitet_datoer.filter(dato__lt=timezone.now().date())
            
            for dato in past_dates:
                for pr in personell_roller:
                    if random() < 0.9:    
                        # 90% chance of staff showing up
                        utbetalt_lonn = random() < 0.5  # 50% chance of having been paid
                        
                        PersonellOppmote.objects.create(
                            aktivitet_datoer=dato,
                            personel_rolle=pr,
                            utbetalt_lonn=utbetalt_lonn
                        )

    def create_betaling_status_drop_in(self):
        self.stdout.write("Creating BetalingStatusDropIn...")
        
        # Get all DeltagerOppmote records where:
        # 1. The member is drop-in
        # 2. They were present
        oppmote_records = DeltagerOppmote.objects.filter(
            medlem_pameldt__drop_in=True,
            tilstede=True
        )
        
        for oppmote in oppmote_records:
            # 80% chance of having paid
            status_betaling = random() < 0.8
            
            # Random discount between 0-20%
            rabatt = round(random() * 0.2, 2) if random() < 0.2 else 0
            
            BetalingStatusDropIn.objects.create(
                deltager_oppmote=oppmote,
                dato=oppmote.aktivitet_datoer.dato,
                rabatt=rabatt,
                status_betaling=status_betaling
            )