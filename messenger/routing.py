from django.urls import re_path

from . import consumers
from . import onlineconsumers

websocket_urlpatterns = [
    re_path(r'ws/socket-server/',consumers.MyConsumer.as_asgi()),
    re_path(r'ws/online/',onlineconsumers.Online.as_asgi()),
]