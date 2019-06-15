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
from home.generate_qr_codes import save_form

import requests
import threading


# Create your views here.
class UrlPage(TemplateView, models.Model):
    template_name = 'url.html'
    
    def get(self, request):
        form = UrlForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self,request):
        form = UrlForm(request.POST)
        url_thread = threading.Thread(target=save_form, args=(form,))
        if form.is_valid():
            values = {'url': form.cleaned_data['url']}
            url_thread.start()
            args = url_qr(values)
            
            return render(request, self.template_name, args)
         
        return render(request, self.template_name, {'form': form})


class VcardPage(TemplateView, models.Model):
    template_name='vcard.html'

    def get(self, request):
        form = VCardForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self,request):
        fields = ['address', 'email', 'name', 'phone', 'country']
        
        if request.POST['action'] == 'upload':
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            
            try:
                with open(filename, 'r') as f:
                    text = self.process_vcard_file()
                    data = {fields[i]: text[i].split(':')[1] for i in range(5)}
                    form = VCardForm(initial = data)     
                return render(request, self.template_name, {'form': form})
            except Exception: 
                if not myfile.name.endswith('.vcf'):
                    return render(request, self.template_name, {'form': form, 'error': 'FileType not valid'})
                else:
                    return render(request, self.template_name, {'form': form, 'error': 'Unkown error'})
        elif request.POST['action'] == 'generate':
            form = VCardForm(request.POST)
            vcard_thread = threading.Thread(target=save_form, args=(form,))

            if form.is_valid():
                values = {fields[i]:form.cleaned_data[fields[i]] for i in range(5)}
                vcard_thread.start()
                args = vcard_qr(values)
                return render(request, self.template_name, args)
            return render(request, self.template_name, {'form': form})
    
    def process_vcard_file(self, f):
        text = f.read()
        text = text.splitlines()
        del text[:2], text[-1]
        text[0] = text[0].replace('\\', '').replace(';', ' ')
        country = text[0].split('   ')[1]
        text[0] = text[0].split('   ')[0]
        text.append('Country:' + country)
        return text
    
class WifiPage(TemplateView, models.Model):
    template_name='wifi.html'

    def get(self, request):
        form = WifiForm(initial={'security': ''})
        return render(request, self.template_name, {'form': form})

    def post(self,request):
        form = WifiForm(request.POST)
        wifi_thread = threading.Thread(target=save_form, args=(form,))
        if form.is_valid():
            values = {
                'ssid': form.cleaned_data['ssid'],
                'security': form.cleaned_data['security'],
                'password': form.cleaned_data['password']
                }
            wifi_thread.start()
            #generate qrcode
            args = wifi_qr(values)
            
            return render(request, self.template_name, args)
        
        return render(request, self.template_name, {'form': form})
