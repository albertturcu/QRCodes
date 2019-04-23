from django import forms
from home.models import Url
from home.models import Vcard
from home.models import Wifi

class HomeForm(forms.ModelForm):
    url = forms.CharField()
    
    class Meta:
        model = Url
        fields = ('url',)

class VCardForm(forms.ModelForm):
    name = forms.CharField()
    email = forms.CharField()
    phone = forms.CharField()
    address=forms.CharField()
    country=forms.CharField()
 
    class Meta:
        model = Vcard
        fields = ('name','email','phone','address','country')

SECURITY_CHOICES=[
    ('No password required'),
    ('WPA/WPA2'),
    ('WEP'),
]
class WifiForm(forms.ModelForm):
    ssid = forms.CharField()
    security = forms.CharField(widget=forms.Select(choices=SECURITY_CHOICES))
    password = forms.CharField()
 
    class Meta:
        model = Wifi
        fields = ('ssid','security','password')
