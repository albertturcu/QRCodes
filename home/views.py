from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.db import models

from home.forms import UrlForm
from home.forms import VCardForm
from home.forms import WifiForm
from home.generate_qr_codes import create_qrcode

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
            form = UrlForm()
            args = create_qrcode(form, values, 'url')
            
            return render(request, self.template_name, args)
         
        return render(request, self.template_name, {'form': form})

class VcardPage(TemplateView):
    template_name='vcard.html'

    def get(self, request):
        form = VCardForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self,request):
        form = VCardForm(request.POST)
        if form.is_valid():
            
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            country = form.cleaned_data['country']

            form = VCardForm()
    
            return render(request, self.template_name, {'qrcode':self.html_img, 'form': form})
    
class WifiPage(TemplateView, models.Model):
    template_name='wifi.html'

    def get(self, request):
        form = WifiForm(initial={'security': ''})
        return render(request, self.template_name, {'form': form})

    def post(self,request):
        form = WifiForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            values = {
                'ssid': form.cleaned_data['ssid'],
                'security': form.cleaned_data['security'],
                'password': form.cleaned_data['password']}
            form = WifiForm()
            
            #generate qrcode
            args = create_qrcode(form, values, 'wifi')
            
            return render(request, self.template_name, args)
        
        return render(request, self.template_name, {'form': form})
