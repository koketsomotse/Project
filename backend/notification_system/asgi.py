"""
ASGI config for notification_system project.

This module configures both HTTP and WebSocket protocols for the application.
It serves as the entry point for ASGI web servers to interact with the application.

The `application` variable is an instance of ProtocolTypeRouter that routes different
protocols (HTTP, WebSocket) to their respective handler applications.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from notifications.routing import websocket_urlpatterns

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notification_system.settings')

# Configure the ASGI application
application = ProtocolTypeRouter({
    # HTTP requests are handled by Django's standard ASGI application
    "http": get_asgi_application(),
    
    # WebSocket requests are handled by Channels
    # AuthMiddlewareStack ensures that we can access the authenticated user in our consumer
    # URLRouter routes WebSocket connections to appropriate consumers based on the URL path
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
