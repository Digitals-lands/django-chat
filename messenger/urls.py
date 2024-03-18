from django.urls import path
from messenger import urls
from .views import *
urlpatterns = [
    path('', register, name='register'),
    path('chat', chat_message, name='chat'),
]
