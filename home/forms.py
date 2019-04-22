from django import forms
from home.models import Url

class HomeForm(forms.ModelForm):
    url = forms.CharField()
    
    class Meta:
        model = Url
        fields = ('url',)