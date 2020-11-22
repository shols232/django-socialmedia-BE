from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
from .token_auth import TokenAuthMiddlewareStack
from django.urls import path, re_path

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': TokenAuthMiddlewareStack(
        URLRouter([
            re_path(r'ws/chat/(?P<room_name>\w+)/$', chat.consumers.ChatConsumer),
            # path('ws/notifications/', account.consumers.NotificationsConsumer),
        ])
    ),
})