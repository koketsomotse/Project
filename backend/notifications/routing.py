"""
WebSocket URL configuration for the notifications app.

This module defines the WebSocket URL patterns that will be used by Django Channels
to route WebSocket connections to the appropriate consumers.

URL Patterns:
    - ws/notifications/: Handles real-time notification updates
"""

from django.urls import re_path
from . import consumers

"""
WebSocket URL configuration for the notifications app.

This module defines the WebSocket URL patterns that will be used by Django Channels
to route WebSocket connections to the appropriate consumers.
"""

websocket_urlpatterns = [
    # WebSocket URL pattern for real-time notifications
    # Path: ws/notifications/
    # Consumer: NotificationsConsumer
    re_path(
        r'ws/notifications/$',  # URL pattern for WebSocket connections
        consumers.NotificationsConsumer.as_asgi(),  # Convert consumer to ASGI application
    ),
]
