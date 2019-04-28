from django import forms
from home.models import Url
from home.models import Vcard
from home.models import Wifi
from home.models import SECURITY_CHOICES


class UrlForm(forms.ModelForm):
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


class WifiForm(forms.ModelForm):
    ssid = forms.CharField(max_length=20)
    security = forms.CharField(widget=forms.Select(choices=SECURITY_CHOICES))
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
 
    class Meta:
        model = Wifi
        fields = ('ssid','security','password')
