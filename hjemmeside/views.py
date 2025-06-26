from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib import messages
from .models import *
from .forms import *

def get_forening_info():
    return ForeningInfo.objects.filter(i_bruk=True).first()


# Views for page
def hjem(request):
    # Hent data fra databasen
    bilder = Bilde.objects.filter(i_bruk=True)
    forening_info = get_forening_info()
    aktiviteter = Aktivitet.objects.all()[:5]
    # aktiviteter = Aktivitet.objects.filter(slutt_dato__gte=now().date())

    if request.method == 'POST':
        
        activity_id = request.POST.get('activity_id')
        if activity_id:
            request.session['selected_activity_id'] = activity_id
            return redirect('pamelding')
    # Pakker de sammen for å sende videre
    pakke = {
        'bilder': bilder,
        'forening_info': forening_info,
        'aktiviteter': aktiviteter,
    }

    return render(request, 'hjemmeside/hjem.html', pakke)

# # This will be removed
def valg(request):

    forening_info = get_forening_info()

    pakke = {
        'page_title': "Påmeldings informasjon",
        'forening_info': forening_info,
    }
    return render(request, 'hjemmeside/valg.html', pakke)

def pamelding(request):

    activity_id = request.session.get('selected_activity_id')
    if not activity_id:
        messages.error(request, "Du må velge en aktivitet først.")
        return redirect('hjem')
                        
    selected_activity = Aktivitet.objects.get(id=activity_id)
    form = AktivitetPamelding()
    forening_info = get_forening_info()

    if request.method == 'POST':
        form = AktivitetPamelding(request.POST)
        if form.is_valid():
            request.session['deltager_navn'] = form.cleaned_data['fornavn'] + " " + form.cleaned_data['etternavn']
            request.session['mail'] = form.cleaned_data['hoved_kontakt_mail']
            request.session['pameldt'] = activity_id
            request.session['source'] = 'pamelding'

            return redirect('bekreftelse')
    

    pakke = {
        'page_title': "Hvem skal meldes på?",
        'selected_activity': selected_activity,
        'forening_info': forening_info,
        'form': form
    }

    return render(request, 'hjemmeside/pamelding.html', pakke)

def kontakt(request):
    form = KundeForesporsel()
    forening_info = get_forening_info()

    if request.method == 'POST':
        form = KundeForesporsel(request.POST)
        if form.is_valid():
            request.session['mail'] = form.cleaned_data['mail']
            request.session['source'] = 'kontakt'

            return redirect('bekreftelse')
    
    pakke = {
        'page_title': "Kontaktskjema",
        'forening_info': forening_info,
        'form': form,
    }

    return render(request, 'hjemmeside/kontakt.html', pakke)

def bekreftelse(request):
    source = request.session.get('source')
    if not source:
        redirect('hjem')

    # Here are the code blocks for the various pages you can come from
    elif source == 'pamelding':
        deltager_navn = request.session.get('deltager_navn')
        mail = request.session.get('mail')
        activity_id = request.session.get('pameldt')
        
        selected_activity = Aktivitet.objects.get(id=activity_id)

        bekreftelse_tekst = f"""
        {deltager_navn} er nå påmeldt {selected_activity}.
        En bekreftelses mail er sendt til {mail}. Dersom du
        ikke finner den så sjekk spam folderen.
        """

    elif source == 'kontakt':
        mail = request.session.get('mail')

        bekreftelse_tekst = f"""
        Din forespørsel er registrert og en bekreftelses mail
        er sendt til {mail}. Dersom du ikke finner den så sjekk
        spam folderen.
        """
        
    forening_info = get_forening_info()

    pakke = {
        'bekreftelse_tekst': bekreftelse_tekst,
        'forening_info': forening_info,
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
