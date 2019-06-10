from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.db import models

from home.forms import UrlForm
from home.forms import VCardForm
from home.forms import WifiForm
from home.generate_qr_codes import url_qr
from home.generate_qr_codes import wifi_qr
from home.generate_qr_codes import vcard_qr

import requests

# Create your views here.
class UrlPage(TemplateView, models.Model):
    template_name = 'url.html'
    
    def get(self, request):
        form = UrlForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self,request):
        form = UrlForm(request.POST)
        if form.is_valid():
            values = {'url': form.cleaned_data['url']}
            args = url_qr(values)
            
            return render(request, self.template_name, args)
         
        return render(request, self.template_name, {'form': form})

class VcardPage(TemplateView):
    template_name='vcard.html'

    def get(self, request):
        form = VCardForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self,request):
        if request.POST['action'] == 'upload':
            data = {'name': '', 'email': '', 'phone': '', 'address': '', 'country': ''}
            
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            
            with open(filename, 'r') as f:
                text = f.read()
                text = text.splitlines()
                data['address'] = text[2].split(';;')[1].replace('\\','')
                data['email'] = text[3].split(':')[1]
                data['name'] = text[4].split(':')[1]
                data['phone'] = text[5].split(':')[1]
                data['country'] = text[2].split(';;')[3].replace(';','')
                
            form = VCardForm(initial = data)
            return render(request, self.template_name, {'form': form})
        elif request.POST['action'] == 'generate':
            form = VCardForm(request.POST)
            if form.is_valid():
                values = {
                    'name': form.cleaned_data['name'],
                    'email': form.cleaned_data['email'],
                    'phone': form.cleaned_data['phone'],
                    'address': form.cleaned_data['address'],
                    'country': form.cleaned_data['country'],
                }

                args = vcard_qr(values)

                return render(request, self.template_name, args)
                  
            return render(request, self.template_name, {'form': form})
    
class WifiPage(TemplateView, models.Model):
    template_name='wifi.html'

    def get(self, request):
        form = WifiForm(initial={'security': ''})
        return render(request, self.template_name, {'form': form})

    def post(self,request):
        form = WifiForm(request.POST)
        if form.is_valid():
            values = {
                'ssid': form.cleaned_data['ssid'],
                'security': form.cleaned_data['security'],
                'password': form.cleaned_data['password']
                }
            
            #generate qrcode
            args = wifi_qr(values)
            
            return render(request, self.template_name, args)
        
        return render(request, self.template_name, {'form': form})
