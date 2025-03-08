from django.urls import path
from . import views

urlpatterns = [
    path('', views.hjem, name='hjemmeside'),
    path('om', views.om, name='om'),
    path('kontakt', views.kontakt, name='kontakt'),
    path('media', views.media, name='media'),
    path('pamelding', views.pamelding, name='pamelding'),
    path('aktiviteter', views.aktiviteter, name='aktiviteter') 
]