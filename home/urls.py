from django.urls import path
from .views import UrlPage
from .views import VcardPage
from .views import WifiPage

urlpatterns = [
    path('wifi/', WifiPage.as_view()),
    path('vcard/', VcardPage.as_view()),
    path('', UrlPage.as_view()),
]
