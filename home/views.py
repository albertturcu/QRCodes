from django.shortcuts import render, redirect
from django.template import loader
from django.views.generic import TemplateView
import pyqrcode
import io
from home.forms import HomeForm
import markdown 

# Create your views here.
class index(TemplateView):
    template_name = 'index.html'
    placeholder_qr = 'https://image.flaticon.com/icons/png/512/107/107072.png'
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
            
            qrcode = pyqrcode.create(text)
            qrcode.png('url.png', scale=5)
            # print(qrcode.terminal(quiet_zone=1))
            image_as_str = qrcode.png_as_base64_str(scale=5)
            html_img = 'data:image/png; base64,{}'.format(image_as_str)
            form = HomeForm()
            
            return render(request, self.template_name, {'qrcode':html_img, 'form': form})

        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)
