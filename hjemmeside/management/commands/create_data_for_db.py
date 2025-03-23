from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, time
from random import choice, randint

from hjemmeside.models import *

class Command(BaseCommand):
    # Help is printed out by terminal when you run the command
    help = "Creates DB data for testing"

    # Handle is a default function in BaseCommand that runs when you run the command
    def handle(self, *args, **kwargs):

        # Making sure there is a superuser
        user = User.objects.filter(username = "admin", is_superuser = True)
        if not user.exists():
            user = User.objects.create_superuser(username = "admin", password = "test")
        # Not sure I need this bit of code
        # else:
        #      user = user.first()

        # End 5/3: generate 1 entry into all of the fields for understanding
        # and then make chat generate a bunch more. As that is not udnerstadning, but busywork.
    
        aktivitets_typer = [
            {"type_aktivitet": "Semesterkurs"},
            {"type_aktivitet": "Feriekurs"},
            {"type_aktivitet": "Jam"},
            {"type_aktivitet": "Samling"}
        ]

        type_liste = []

        for i in aktivitets_typer:
            type_liste.append(TypeAktivitet.objects.create(**i))

        aktivitets_steder = [
            { "omrade": "Nesttun", "oppmote_sted": "Foran Fana Kulturhus"},
            { "omrade": "Olsvik", "oppmote_sted": "Olsvik parkour park"},
            { "omrade": "Åsane", "oppmote_sted": "Fysak Åsane 2.etg"},
            { "omrade": "Bergen Sentrum", "oppmote_sted": "Etter beskjed"},
        ]

        steder_liste = []

        for i in aktivitets_steder:
            steder_liste.append(StedAktivitet.objects.create(**i))

        aktivitets_malgruppe = [
            { "alder_eller_klasse": "1-3.kl", "vanskelighetsgrad_eller_formål": "Blandet"},
            { "alder_eller_klasse": "4-7.kl", "vanskelighetsgrad_eller_formål": "Blandet"},
            { "alder_eller_klasse": "8.kl+", "vanskelighetsgrad_eller_formål": "Blandet"},
            { "alder_eller_klasse": "5-7.kl", "vanskelighetsgrad_eller_formål": "Viderekomen"},
            { "alder_eller_klasse": "5-10.kl", "vanskelighetsgrad_eller_formål": "Teknisk"},
            { "alder_eller_klasse": "1.vgs+", "vanskelighetsgrad_eller_formål": "Teknisk"},
            { "alder_eller_klasse": "Voksne", "vanskelighetsgrad_eller_formål": "Blandet"}
        ]

        malgruppe_liste = []

        for i in aktivitets_malgruppe:
            malgruppe_liste.append(MalgruppeAktivitet.objects.create(**i))

        datoer_som_utgar = [
            { "dato": date(2025, 2, 27), "begrunnelse": "Vinterferie"},
            { "dato": date(2025, 4, 14), "begrunnelse": "Påske"},
            { "dato": date(2025, 4, 15), "begrunnelse": "Påske"},
            { "dato": date(2025, 4, 16), "begrunnelse": "Påske"},
            { "dato": date(2025, 4, 17), "begrunnelse": "Påske"},
            { "dato": date(2025, 4, 18), "begrunnelse": "Påske"},
            { "dato": date(2025, 4, 21), "begrunnelse": "Påske"},
            { "dato": date(2025, 5, 1), "begrunnelse": "Helligdag"},
            { "dato": date(2025, 5, 2), "begrunnelse": "Planleggingsdag"},
            { "dato": date(2025, 5, 29), "begrunnelse": "Helligdag"},
            { "dato": date(2025, 5, 30), "begrunnelse": "Planleggingsdag"},
        ]

        datoer_liste= []

        for i in datoer_som_utgar:
            datoer_liste.append(DatoerSomUtgar.objects.create(**i))

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

        personell_liste = []

        for i in personell:
            personell_liste.append(Personell.objects.create(**i))

        rolle = [
            {"rolle": "Instruktør", "lonn": 300},
            {"rolle": "Assistent", "lonn": 250},
            {"rolle": "Ansvarlig", "lonn": 300},
            {"rolle": "Hovedinstruktør", "lonn": 650},
            {"rolle": "Frivillig", "lonn": 0}
        ]

        rolle_liste = []

        for i in rolle:
            rolle_liste.append(Rolle.objects.create(**i))

        # 0-12: 0-3 = Nesttun, 4-6 = Olsvik, 7-9 =  Åsane, 10-11 = Tek, 12 = Vo
        aktivitet = [
            {"type_aktivitet": 0, "sted": 0, "malgruppe": 0, "oppstart": date(2025, 3, 3),
             "slutt": date(2025, 6, 2), "kl_start": time(17), "kl_slutt": time(18),
              "antall_ganger": 12, "pris": 1300, "datoer_som_utgar": [1,6]},
            {"type_aktivitet": 0, "sted": 0, "malgruppe": 1, "oppstart": date(2025, 3, 3),
             "slutt": date(2025, 6, 2), "kl_start": time(18), "kl_slutt": time(19),
              "antall_ganger": 12, "pris": 1300, "datoer_som_utgar": [1,6]},
            {"type_aktivitet": 0, "sted": 0, "malgruppe": 3, "oppstart": date(2025, 3, 3),
             "slutt": date(2025, 6, 2), "kl_start": time(19), "kl_slutt": time(20),
              "antall_ganger": 12, "pris": 1300, "datoer_som_utgar": [1,6]},
            {"type_aktivitet": 0, "sted": 0, "malgruppe": 2, "oppstart": date(2025, 3, 3),
             "slutt": date(2025, 6, 2), "kl_start": time(20), "kl_slutt": time(21),
              "antall_ganger": 12, "pris": 1300, "datoer_som_utgar": [1,6]},
            {"type_aktivitet": 0, "sted": 1, "malgruppe": 0, "oppstart": date(2025, 3, 4),
             "slutt": date(2025, 5, 27), "kl_start": time(17), "kl_slutt": time(18),
              "antall_ganger": 12, "pris": 0, "datoer_som_utgar": 2},
            {"type_aktivitet": 0, "sted": 1, "malgruppe": 1, "oppstart": date(2025, 3, 4),
             "slutt": date(2025, 5, 27), "kl_start": time(18), "kl_slutt": time(19),
              "antall_ganger": 12, "pris": 0, "datoer_som_utgar": 2},
            {"type_aktivitet": 0, "sted": 1, "malgruppe": 3, "oppstart": date(2025, 3, 4),
             "slutt": date(2025, 5, 27), "kl_start": time(19), "kl_slutt": time(20),
              "antall_ganger": 12, "pris": 0, "datoer_som_utgar": 2},
            {"type_aktivitet": 0, "sted": 2, "malgruppe": 0, "oppstart": date(2025, 3, 5),
             "slutt": date(2025, 6, 4), "kl_start": time(17), "kl_slutt": time(18),
              "antall_ganger": 13, "pris": 1400, "datoer_som_utgar": 3},
            {"type_aktivitet": 0, "sted": 2, "malgruppe": 1, "oppstart": date(2025, 3, 5),
             "slutt": date(2025, 6, 4), "kl_start": time(18), "kl_slutt": time(19),
              "antall_ganger": 13, "pris": 1400, "datoer_som_utgar": 3},
            {"type_aktivitet": 0, "sted": 2, "malgruppe": 2, "oppstart": date(2025, 3, 5),
             "slutt": date(2025, 6, 4), "kl_start": time(19), "kl_slutt": time(20),
              "antall_ganger": 13, "pris": 1400, "datoer_som_utgar": 3},
            {"type_aktivitet": 0, "sted": 3, "malgruppe": 4, "oppstart": date(2025, 1, 23),
             "slutt": date(2025, 6, 5), "kl_start": time(16, 30), "kl_slutt": time(18),
              "antall_ganger": 16, "pris": 1750, "datoer_som_utgar": [0,4,7,9]},
            {"type_aktivitet": 0, "sted": 3, "malgruppe": 5, "oppstart": date(2025, 1, 23),
             "slutt": date(2025, 6, 5), "kl_start": time(18, 30), "kl_slutt": time(20),
              "antall_ganger": 16, "pris": 1750, "datoer_som_utgar": [0,4,7,9]},
            {"type_aktivitet": 0, "sted": 3, "malgruppe": 6, "oppstart": date(2025, 1, 24),
             "slutt": date(2025, 6, 6), "kl_start": time(18), "kl_slutt": time(19, 30),
              "antall_ganger": 12, "pris": 1300, "datoer_som_utgar": [5,8,10]},
        ]

        aktivitet_liste = []

        for a in aktivitet:
            aktivitet = Aktivitet.objects.create(
                type_aktivitet = type_liste[a["type_aktivitet"]],
                sted = steder_liste[a["sted"]],
                malgruppe = malgruppe_liste[a["malgruppe"]],
                oppstart = a["oppstart"],
                slutt = a["slutt"],
                kl_start = a["kl_start"],
                kl_slutt = a["kl_slutt"],
                antall_ganger = a["antall_ganger"],
                pris = a["pris"],
            )

            dato_indexes = a["datoer_som_utgar"] if isinstance(a["datoer_som_utgar"], list) else [a["datoer_som_utgar"]]
            datoer = [datoer_liste[i] for i in a["datoer_som_utgar"]]

            aktivitet.datoer_som_utgar.set(datoer)

            aktivitet_liste.append(aktivitet)

        aktivitet_personell = [
            { "aktivitet": 0, "personell": 1, "rolle": 0},
            { "aktivitet": 0, "personell": 2, "rolle": 1},
            { "aktivitet": 1, "personell": 1, "rolle": 0},
            { "aktivitet": 1, "personell": 2, "rolle": 1},
            { "aktivitet": 2, "personell": 3, "rolle": 0},
            { "aktivitet": 2, "personell": 4, "rolle": 0},
            { "aktivitet": 3, "personell": 3, "rolle": 0},
            { "aktivitet": 3, "personell": 4, "rolle": 0},
            { "aktivitet": 4, "personell": 5, "rolle": 0},
            { "aktivitet": 4, "personell": 6, "rolle": 4},
            { "aktivitet": 5, "personell": 5, "rolle": 0},
            { "aktivitet": 5, "personell": 6, "rolle": 4},
            { "aktivitet": 6, "personell": 5, "rolle": 0},
            { "aktivitet": 6, "personell": 6, "rolle": 4},
            { "aktivitet": 7, "personell": 5, "rolle": 0},
            { "aktivitet": 7, "personell": 7, "rolle": 1},
            { "aktivitet": 8, "personell": 5, "rolle": 0},
            { "aktivitet": 8, "personell": 1, "rolle": 2},
            { "aktivitet": 8, "personell": 7, "rolle": 1},
            { "aktivitet": 9, "personell": 5, "rolle": 0},
            { "aktivitet": 9, "personell": 7, "rolle": 1},
            { "aktivitet": 10, "personell": 0, "rolle": 3},
            { "aktivitet": 11, "personell": 0, "rolle": 3},
            { "aktivitet": 12, "personell": 0, "rolle": 3},
        ]

        aktivitet_personell_liste = []

        for a in aktivitet_personell:
            aktivitet_person = AktivitetPersonell.objects.create(
                aktivitet = aktivitet_liste[a["aktivitet"]],
                personell = personell_liste[a["personell"]],
                rolle = rolle_liste[a["rolle"]]
            )


        # Data pools
        addresses = ["Parkveien 1", "Hovedgaten 45", "Lillebakken 12", "Strandveien 78", "Sentrum 9", "Bakkeveien 22", "Skogstien 33", "Elveveien 19"]
        post_numbers = ["5000", "5010", "5020", "5030", "5040", "5050", "5060", "5070"]
        emails = ["kontakt1@mail.com", "kontakt2@mail.com", "kontakt3@mail.com", "kontakt4@mail.com", "hjelp@mail.com", "info@mail.com", "kontakt@eksempel.no", "post@forening.no"]
        first_names = ["Anna", "Bjørn", "Clara", "Daniel", "Emil", "Frida", "Gunnar", "Hanna", "Ivar", "Jenny"]
        last_names = ["Hansen", "Olsen", "Nilsen", "Johansen", "Larsen", "Andersen", "Pedersen", "Bakke", "Svendsen", "Solberg"]
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

        medlem_liste = []

        for aktivitet in aktivitet_liste:
            malgruppe = aktivitet.malgruppe.alder_eller_klasse
            age_range = age_map.get(malgruppe, (10, 15))

            for _ in range(5):
                fornavn = choice(first_names)
                etternavn = choice(last_names)
                alder = randint(age_range[0], age_range[1])
                fodt_ar = date.today().year - alder
                adresse = choice(addresses)
                post_nr = choice(post_numbers)

                hoved_kontakt_tlf = f"9{randint(1000000, 9999999)}"
                hoved_kontakt_mail = choice(emails)
                hoved_kontakt_rolle = choice(kontakter_roller)

                medlem = Medlem.objects.create(
                    fornavn=fornavn,
                    etternavn=etternavn,
                    alder=alder,
                    fodt_ar=fodt_ar,
                    adresse=adresse,
                    post_nummer=post_nr,
                    foto_tillatelse=choice([True, False]),
                    hoved_kontakt_tlf=hoved_kontakt_tlf,
                    hoved_kontakt_mail=hoved_kontakt_mail,
                    hoved_kontakt_rolle=hoved_kontakt_rolle,
                    annet=""
                )
                medlem.pameldt.add(aktivitet)

                for nr in range(2, 4):
                    if choice([True, False]):
                        setattr(medlem, f"kontakt{nr}_tlf", f"9{randint(1000000, 9999999)}")
                        setattr(medlem, f"kontakt{nr}_mail", choice(emails))
                        setattr(medlem, f"kontakt{nr}_rolle", choice(kontakter_roller))
                medlem.save()
                medlem_liste.append(medlem)

        for _ in range(randint(5, 10)):
            MeldtInteresse.objects.create(
                mail=choice(emails),
                tlf=f"9{randint(1000000, 9999999)}",
                oppsummert=choice(["Ønske om kurs", "Spørsmål om treninger", "Lurer på medlemskap"]),
                detaljer=choice([
                    "Vil gjerne delta på kommende kurs.",
                    "Når starter neste kurs for barn?",
                    "Hvordan melder man seg inn?",
                    "Er det ledig plass på kurset i Åsane?",
                    "Ønsker info om familiekurs."
                ]),
            )

        for _ in range(randint(5, 10)):
            KontakterForening.objects.create(
                mail=choice(emails),
                tlf=f"9{randint(1000000, 9999999)}",
                oppsummert=choice(["Forespørsel om informasjon", "Spørsmål om samarbeid", "Generell kontakt"]),
                detaljer=choice([
                    "Vil vite mer om foreningen.",
                    "Ønsker samarbeid med foreningen.",
                    "Hvordan kan man bidra frivillig?",
                    "Trenger informasjon om parkour tilbud."
                ]),
            )


        # Create Oppmøte records for each member in their activities
        for medlem in medlem_liste:
            for akt in medlem.pameldt.all():
                Oppmote.objects.create(aktivitet=akt, medlem=medlem)

        # Create KontaktListe records for each member in their activities
        for medlem in medlem_liste:
            for akt in medlem.pameldt.all():
                KontaktListe.objects.create(aktivitet=akt, medlem=medlem)