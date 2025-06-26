from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.hjem, name='hjem'),
    path('valg', views.valg, name='valg'),
    path('pamelding', views.pamelding, name='pamelding'),
    path('kontakt', views.kontakt, name='kontakt'),
    path('bekreftelse', views.bekreftelse, name='bekreftelse'),
    path('instagram', views.instagram_redirect, name='instagram'),
    path('facebook', views.facebook_redirect, name='facebook')
]
