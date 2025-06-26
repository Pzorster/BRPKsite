from django import forms
from .models import Medlem, KundeKontakt

class AktivitetPamelding(forms.ModelForm):
    class Meta:
        model = Medlem
        fields = '__all__'
        exclude = ['notater']


class KundeForesporsel(forms.ModelForm):
    class Meta:
        model = KundeKontakt
        fields = '__all__'
        exclude = ['fulgt_opp']