from django.urls import re_path
from notifications.consumers import NotificationsConsumer
from notifications.middleware import TokenAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddleware(
        URLRouter(
            [
                re_path(r'ws/notifications/$', NotificationsConsumer.as_asgi()),
            ]
        )
    ),
})
