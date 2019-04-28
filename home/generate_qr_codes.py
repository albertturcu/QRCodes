from home.forms import UrlForm
from home.forms import VCardForm
from home.forms import WifiForm

import requests
import io
import base64
import pyqrcode

def create_qrcode(form , args: dict, qr_type: str):
    if qr_type == 'url':
        qrcode = pyqrcode.create(args['url'])
    elif qr_type == 'vcard':
        pass
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

    args = {'form': form, 'qrcode': html_img,
            'qrcodesvg': html_img2, 'qrcodeeps': html_img3}
    
    return args
