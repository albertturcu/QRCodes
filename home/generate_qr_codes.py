from home.forms import UrlForm
from home.forms import VCardForm
from home.forms import WifiForm

import requests
import io
import base64
import pyqrcode
import vobject 

def create_qrcode(form , args: dict, qr_type: str):
    context = {}
    if qr_type == 'url':
        qrcode = pyqrcode.create(args['url'])
    elif qr_type == 'vcard':
        vcard_string = create_vcard(args)
        print(vcard_string)
        qrcode = pyqrcode.create(vcard_string)
        with open('vcard.vcf', 'w') as f:
            f.write(vcard_string)
            context = {'vcard': f}
    elif qr_type == 'wifi':
        qrcode = pyqrcode.create(
            f"WIFI:S:{args['ssid']};T:{args['security']};P:{args['password']};;")

    image_as_str = qrcode.png_as_base64_str(scale=5)
    bytes_buf = io.BytesIO()
    string_buf = io.StringIO()
    qrcode.svg(bytes_buf, scale=5)
    qrcode.eps(string_buf, scale=5)

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

    
    
    
