from django.test import TestCase
from home.forms import UrlForm

class TestForms(TestCase):
    
    def test_url_form_valid_data(self):
        form = UrlForm(data={
            'url': 'google.com'
        })

        self.assertTrue(form.is_valid())
        
    def test_url_form_no_data(self):
        form = UrlForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)