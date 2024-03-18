from django.urls import path
from messenger import urls
from .views import *
urlpatterns = [
    
    path('', register),
    path('login', login),
]
