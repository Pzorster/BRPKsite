from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib import messages
from django.core.mail import send_mail
from .models import *
from .forms import *
from datetime import datetime, date
from decouple import config

def get_forening_info():
    forening_info = ForeningInfo.objects.filter(i_bruk=True).first()
    return forening_info

# Here we load in data that is the same across the site.
# Linked through settings.py/TEMPLATES/OPTIONS/context_processors
def global_site_context(request):

    # .logo is set for 4 menu bar items in wide view. More items and it will crash into them before
    # @media (min-width: 1000px) kicks in. FFP.
    menu_items = [
    {'name': 'Hjem', 'url': 'hjem'},
    {'name': 'Timeplan', 'url': 'hjem', 'anchor': 'aktiviteter'},
    # {'name': 'Aktiviteter', 'has_dropdown': True, 'dropdown_items':[
    #     {'name': 'Påmelding', 'url': 'kurs_valg'},
    #     {'name': 'Timeplan', 'url': 'hjem', 'anchor': 'aktiviteter'},
    # ]},
    {'name': 'Om oss', 'url': 'hjem', 'anchor': 'om-oss'},
    {'name': 'Kontakt', 'url': 'kontakt'},
    ]
   
    footer_info = get_forening_info()

    site_data = {
        'menu_items': menu_items,
        'footer_info': footer_info,
    }

    return site_data


def hjem(request):

    if request.method == 'POST':
        activity_id = request.POST.get('activity_id')
        if activity_id:
            request.session['selected_activity_id'] = activity_id
            return redirect('pamelding')
        

    bilder = Bilde.objects.filter(i_bruk=True).order_by('rekkefolge')
    aktiviteter = Aktivitet.objects.all()

    pakke = {
        'bilder': bilder,
        'semesterkurs': [],
        'feriekurs': [],
        'andre': []
    }

    for aktivitet in aktiviteter:
        activity_type = aktivitet.type_aktivitet.type_aktivitet
        if activity_type == 'Semesterkurs':
            pakke['semesterkurs'].append(aktivitet)
        elif activity_type == 'Feriekurs':
            pakke['feriekurs'].append(aktivitet)
        else:
            pakke['andre'].append(aktivitet)

    return render(request, 'hjemmeside/hjem.html', pakke)



# def kurs_valg(request):

#     if request.method == 'POST':
#         activity_id = request.POST.get('activity_id')
#         if activity_id:
#             request.session['selected_activity_id'] = activity_id
#             return redirect('pamelding')
        

#     aktiviteter = Aktivitet.objects.all()#[:10]

#     def get_nested_attr(obj, attr_path):
#         attrs=attr_path.split('.')
#         for attr in attrs:
#             obj = getattr(obj, attr)
#         return obj

#     attr_filter = {
#         'Alder': 'malgruppe.alder_eller_klasse', 
#         'Sted': 'sted.omrade',
#         'Ukedag': 'ukedag',
#         }
    
#     filtre = {}

#     for filter_name, attr_path in attr_filter.items():
#         if filter_name not in filtre:
#             filtre[filter_name] = set()
        
#         for aktivitet in aktiviteter:
#             try:
#                 value = get_nested_attr(aktivitet, attr_path)
#                 filtre[filter_name].add(value)
#             except AttributeError:
#                 print(f"Could not access {attr_path} on {aktivitet}")

#     for filter_name in filtre:
#         filtre[filter_name] = {
#             'label': filter_name,
#             'values': sorted(list(filtre[filter_name]))
#         }

#     aktiviteter_with_data = []
#     for aktivitet in aktiviteter:
#         data_attrs = {}
#         for data_key, attr_path in attr_filter.items():
#             try:
#                 data_attrs[data_key] = get_nested_attr(aktivitet, attr_path)
#             except AttributeError:
#                 data_attrs[data_key]= ""

#         aktiviteter_with_data.append({
#             'aktivitet': aktivitet,
#             'data_attrs': data_attrs,
#         })

#     pakke = {
#         'aktiviteter_with_data': aktiviteter_with_data,
#         'filtre': filtre,
#     }
    
#     return render(request, 'hjemmeside/kurs_valg.html', pakke)



def pamelding(request):

    activity_id = request.session.get('selected_activity_id')
    if not activity_id:
        messages.error(request, "Du må velge en aktivitet først.")
        return redirect('hjem')
                        
    selected_activity = Aktivitet.objects.get(id=activity_id)
    form = AktivitetPamelding()

    if request.method == 'POST':
        form = AktivitetPamelding(request.POST)
        if form.is_valid():

            serializable_data = {}
            for field_name, value in form.cleaned_data.items():
                if isinstance(value, date):  # If it's a date object
                    serializable_data[field_name] = value.isoformat()  # Convert to string like "1990-05-15"
                else:
                    serializable_data[field_name] = value

            request.session['pameldt'] = activity_id
            request.session['source'] = 'pamelding'
            request.session['form_data'] = serializable_data

            return redirect('bekreftelse')
    

    pakke = {
        'page_title': "Hvem skal meldes på?",
        'selected_activity': selected_activity,
        'form': form
    }

    return render(request, 'hjemmeside/pamelding.html', pakke)

def kontakt(request):
    form = KundeForesporsel()

    if request.method == 'POST':
        form = KundeForesporsel(request.POST)
        if form.is_valid():

            serializable_data = {}
            for field_name, value in form.cleaned_data.items():
                if hasattr(value, 'pk'):  # If it's a model object
                    serializable_data[field_name] = value.pk  # Store just the ID
                else:
                    serializable_data[field_name] = value

            request.session['form_data'] = serializable_data
            request.session['source'] = 'kontakt'

            return redirect('bekreftelse')
    
    pakke = {
        'page_title': "Kontaktskjema",
        'form': form,
    }

    return render(request, 'hjemmeside/kontakt.html', pakke)

def bekreftelse(request):
    source = request.session.get('source')
    if not source:
        redirect('hjem')

    form_data = request.session.get('form_data').copy()

    # Here are the code blocks for the various pages you can come from
    if source == 'pamelding':
        if 'fodt_ar' in form_data and isinstance(form_data['fodt_ar'], str):
            form_data['fodt_ar'] = datetime.fromisoformat(form_data['fodt_ar']).date()
    
        form = AktivitetPamelding(data=form_data) 
        if form.is_valid():
            medlem = form.save()
            print(f"Saved member: {medlem.id}")
            deltager_navn = form_data.get('fornavn') + " " + form_data.get('etternavn')
            mail = form_data.get('hoved_kontakt_mail')
            activity_id = request.session.get('pameldt')
            
            selected_activity = Aktivitet.objects.get(id=activity_id)

            bekreftelse_tekst = f"""
            {deltager_navn} er nå påmeldt {selected_activity}.
            En bekreftelses mail er sendt til {mail}. Dersom du
            ikke finner den så sjekk spam folderen.
            """

            del request.session['form_data']
            del request.session['pameldt']
            del request.session['source']

    elif source == 'kontakt':
        if 'kategori' in form_data:  # or whatever your ForeignKey field is called
            kategori_id = form_data['kategori']
            form_data['kategori'] = ForesporselKategori.objects.get(id=kategori_id)
    
        form = KundeForesporsel(data=form_data) 
        if form.is_valid():
            kundekontakt = form.save()

            send_mail(
            subject='Takk for din henvendelse',
            message=f'''
Hei {kundekontakt.navn} :)

Vi har mottatt din forespørsel angående {str(kundekontakt.kategori).lower()}. Vi svarer som oftest en gang i uken.
Om vi trenger å ta kontakt direkte så ringer vi på {kundekontakt.tlf}.

Med vennlig hilsen,
Bergen Parkour

Informasjonen vi fikk fra deg: "{kundekontakt.detaljer}"''',
            from_email='bergen.parkour@gmail.com',
            recipient_list=[kundekontakt.mail],
            fail_silently=False,  # Will raise error if email fails
            )

            mail = form_data.get('mail')

            bekreftelse_tekst = f"""
            Forespørsel er registrert og en bekreftelses mail
            er sendt til {mail}. Dersom du ikke finner den sjekk
            spam folderen.
            """
            
            del request.session['form_data']
        

    pakke = {
        'bekreftelse_tekst': bekreftelse_tekst,
    }

    return render(request, 'hjemmeside/bekreftelse.html', pakke)

def instagram_redirect(request):
    forening_info = get_forening_info() 
    instagram = 'https://www.instagram.com/'+forening_info.instagram_side
    return redirect(instagram)

def facebook_redirect(request):
    forening_info = get_forening_info() 
    facebook = 'https://www.facebook.com/'+forening_info.facebook_side
    return redirect(facebook)
