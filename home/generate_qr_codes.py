from home.forms import UrlForm
from home.forms import VCardForm
from home.forms import WifiForm

import requests
import io
import base64
import pyqrcode
import vobject 


def url_qr(context: dict):
    form =  UrlForm()
    qrcode = pyqrcode.create(context['url'])
    return create_qrcode(form, context, qrcode)


def vcard_qr(context: dict):
    form = VCardForm()
    vcard_string = create_vcard(context)
    qrcode = pyqrcode.create(vcard_string)
    context = {**context,**{'vcard': 'data:text/plain; base64,{}'.format(base64.b64encode(io.BytesIO(bytes(vcard_string, encoding='utf-8')).getvalue()).decode('utf-8'))}}
    return create_qrcode(form, context, qrcode)


def wifi_qr(context: dict):
    form = WifiForm()
    qrcode = pyqrcode.create(
        f"WIFI:S:{context['ssid']};T:{context['security']};P:{context['password']};;")
    return create_qrcode(form, context, qrcode)

def create_qrcode(form, context: dict, *args):
       
    image_as_str = args[0].png_as_base64_str(scale=5)
    bytes_buf = io.BytesIO()
    string_buf = io.StringIO()
    args[0].svg(bytes_buf, scale=5)
    args[0].eps(string_buf, scale=5)

    html_img = 'data:image/png; base64,{}'.format(image_as_str)
    html_img2 = 'data:image/svg; base64,{}'.format(
        base64.b64encode(bytes_buf.getvalue()).decode('utf-8'))
    html_img3 = 'data:image/eps; base64,{}'.format(base64.b64encode(
        string_buf.getvalue().encode('utf-8')).decode('utf-8'))

    context = {**context, **{'form': form, 'qrcode': html_img,
            'qrcodesvg': html_img2, 'qrcodeeps': html_img3}}
    return context

def create_vcard(args: dict):
    vcard = vobject.vCard()
    vcard.add('fn')
    vcard.fn.value = args['name']
    vcard.add('email')
    vcard.email.value = args['email']
    vcard.email.type_param = 'INTERNET'
    vcard.add('tel')
    vcard.tel.value = args['phone']
    vcard.tel.type_param = 'MOBILE'
    vcard.add('adr')
    vcard.adr.value = vobject.vcard.Address(street= args['address'], country = args['country'])

    return vcard.serialize()

    
    
    
