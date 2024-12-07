"""
ASGI Configuration

This module configures ASGI (Asynchronous Server Gateway Interface)
for the notification system. It handles both HTTP and WebSocket protocols
using Django Channels.

The application is configured to:
1. Handle HTTP requests through Django's standard ASGI application
2. Route WebSocket connections through the notification system's consumers
3. Apply authentication middleware to all connections
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from notifications.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notification_system.settings')

application = ProtocolTypeRouter({
    # Handle regular HTTP requests
    "http": get_asgi_application(),
    
    # Handle WebSocket connections
    "websocket": AuthMiddlewareStack(
        URLRouter(
            # Use the WebSocket URL patterns from the notifications app
            websocket_urlpatterns
        )
    ),
})