from django.urls import path
from .views import index
from .views import VcardPage
from .views import WifiPage

urlpatterns = [
    path('wifi/', WifiPage.as_view()),
    path('vcard/', VcardPage.as_view()),
    path('', index.as_view()),
]
