import os
from django.urls import path
from chat_app import consumers
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application



ws_routers = [
    path("chat/<str:username>/",consumers.SingleChatConsumer.as_asgi()),
    path("group/<int:id>/",consumers.GroupChat.as_asgi()),
 
]


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            ws_routers
        )
    ),
})