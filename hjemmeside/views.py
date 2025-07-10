from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib import messages
from django.core.mail import send_mail
from .models import *
from .forms import *
from datetime import datetime, date

def get_forening_info():
    forening_info = ForeningInfo.objects.filter(i_bruk=True).first()
    return forening_info

# Here we load in data that is the same across the site.
# Linked through settings.py/TEMPLATES/OPTIONS/context_processors
def global_site_context(request):

    menu_items = [
    {'name': 'Hjem', 'url': 'hjem'},
    {'name': 'Aktiviteter', 'has_dropdown': True, 'dropdown_items': [
        {'name': 'Påmelding', 'url': 'kurs_valg'},
        {'name': 'Timeplan', 'url': 'timeplan'},
    ]},
    {'name': 'Om oss', 'url': 'om_foreningen'},
    {'name': 'Kontakt', 'url': 'kontakt'},
    ]
   
    footer_info = get_forening_info()

    site_data = {
        'menu_items': menu_items,
        'footer_info': footer_info,
    }

    return site_data



# Views for page
def hjem(request):
    # Hent data fra databasen
    bilder = Bilde.objects.filter(i_bruk=True)
    aktiviteter = Aktivitet.objects.all()[:10]
    # aktiviteter = Aktivitet.objects.filter(slutt_dato__gte=now().date())

    if request.method == 'POST':
        
        activity_id = request.POST.get('activity_id')
        if activity_id:
            request.session['selected_activity_id'] = activity_id
            return redirect('pamelding')
    # Pakker de sammen for å sende videre
    pakke = {
        'bilder': bilder,
        'aktiviteter': aktiviteter,
    }

    return render(request, 'hjemmeside/hjem.html', pakke)



def kurs_valg(request):

    pakke = {
        'page_title': "Påmeldings informasjon",
    }
    return render(request, 'hjemmeside/kurs_valg.html', pakke)



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



def timeplan(request):

    pakke = {

    }

    return render(request, 'hjemmeside/timeplan.html', pakke)



def om_foreningen(request):

    pakke = {

    }

    return render(request, 'hjemmeside/om_foreningen.html', pakke)



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
            print(f"Saved member: {kundekontakt.id}")
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
