from django.urls import path
from . import consumer


websocket_urlpatterns = [
    path('ws/message/group/<str:blog_title>', consumer.MessageConsumer.as_asgi()),
]
