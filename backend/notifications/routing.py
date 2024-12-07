from django.urls import re_path
from . import consumers

"""
WebSocket URL Configuration

This module defines the WebSocket URL patterns for the notification system.
Each URL pattern maps to a specific consumer that handles the WebSocket connection.

URL Patterns:
    - ws/notifications/: Handles real-time notifications for authenticated users
"""

websocket_urlpatterns = [
    re_path(
        r'ws/notifications/$',
        consumers.NotificationsConsumer.as_asgi(),
        name='notifications'
    ),
]