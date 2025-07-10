from django import forms
from .models import Medlem, KundeKontakt

class AktivitetPamelding(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = "" 
        
    class Meta:
        model = Medlem
        fields = '__all__'
        exclude = ['notater']


class KundeForesporsel(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = "" 

    class Meta:
        model = KundeKontakt
        fields = '__all__'
        exclude = ['fulgt_opp']