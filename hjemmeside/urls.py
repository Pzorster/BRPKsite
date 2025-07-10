from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.hjem, name='hjem'),
    path('kurs_valg', views.kurs_valg, name='kurs_valg'),
    path('pamelding', views.pamelding, name='pamelding'),
    path('timeplan', views.timeplan, name='timeplan'),
    path('om_foreningen', views.om_foreningen, name='om_foreningen'),
    path('kontakt', views.kontakt, name='kontakt'),
    path('bekreftelse', views.bekreftelse, name='bekreftelse'),
    path('instagram', views.instagram_redirect, name='instagram'),
    path('facebook', views.facebook_redirect, name='facebook'),
]
