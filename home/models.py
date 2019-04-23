from django.db import models

# Create your models here.
class Url(models.Model):
    url = models.CharField(max_length=100)
    qrcode = models.CharField(max_length=1000)

class Vcard(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    country=models.CharField(max_length=100)

class Wifi(models.Model):
    ssid = models.CharField(max_length=100)
    security = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    
