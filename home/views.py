from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views.generic import TemplateView
import pyqrcode
import io
from home.forms import HomeForm

# Create your views here.
class index(TemplateView):
    template_name = 'index.html'
        
    def get(self, request):
        form = HomeForm()
        return render(request, self.template_name, {'form': form})

    # def generate_url_qrcode(self,request):
    #     template = loader.get_template('home/index.html')
    #     img_string = io.StringIO()
    #     qrcode = pyqrcode.create('google.com')
    #     qrcode.png(img_string, scale=5)
    #     # return render(request, 'index.html', img)
    #     return HttpResponse(template.render(request,body=img_string.getvalue(), content_type="image/png", content_disposition='attachment; filename="url.png"'))

    def post(self,request):
        form = HomeForm(request.POST)
        if form.is_valid():
            form.save()
            text = form.cleaned_data['url']
            form = HomeForm()
            return redirect('/')

        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)