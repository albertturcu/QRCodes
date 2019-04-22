from django.shortcuts import render, redirect
from django.views.generic import TemplateView
import pyqrcode
from home.forms import HomeForm
from django.db import models
from home.models import Url

# Create your views here.
class index(TemplateView, models.Model):
    template_name = 'index.html'
    html_img = ''
    
    def get(self, request):
        form = HomeForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self,request):
        form = HomeForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['url']
            
            qrcode = pyqrcode.create(text)
            qrcode.png('url.png', scale=5)
            
            image_as_str = qrcode.png_as_base64_str(scale=5)
            self.html_img = 'data:image/png; base64,{}'.format(image_as_str)
            
            url_db = Url(url=text, qrcode = self.html_img)
            url_db.save()
            
            form = HomeForm()
    
            return render(request, self.template_name, {'qrcode':self.html_img, 'form': form})

        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)
    
        
        
