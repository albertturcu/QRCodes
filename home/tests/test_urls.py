from django.test import TestCase
from django.urls import reverse, resolve 
from home.views import UrlPage, WifiPage, VcardPage

class TestUrls(TestCase):
    
    def test_urlqr_urls_is_resolved(self):
        url = reverse('')
        self.assertEquals(resolve(url).func.view_class, UrlPage)
        
    def test_urlwifi_urls_is_resolved(self):
        url = reverse('wifi')
        self.assertEquals(resolve(url).func.view_class, WifiPage)
        
    def test_urlvcard_urls_is_resolved(self):
        url = reverse('vcard')
        self.assertEquals(resolve(url).func.view_class, VcardPage)
