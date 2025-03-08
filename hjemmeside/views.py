from django.shortcuts import render

# Create your views here.

def hjem(request):
    return render(request, 'hjemmeside/hjem.html')

def om(request):
    return render(request, 'hjemmeside/om.html')

def kontakt(request):
    return render(request, 'hjemmeside/kontakt.html')

def media(request):
    return render(request, 'hjemmeside/media.html')

def pamelding(request):
    return render(request, 'hjemmeside/pamelding.html')

def aktiviteter(request):
    return render(request, 'hjemmeside/aktiviteter.html')
