from django.urls import path
from messenger import urls
from .views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', register, name='register'),
    path('chat', chat_message, name='chat'),
    path('login', login_user, name='login'),
    path('deconnexion', deconnexion, name='deconnexion'),
    path('send-message', send_message, name='send_message'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)