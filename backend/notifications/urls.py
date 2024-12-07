from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

"""
API URL Configuration

This module defines the URL patterns for the notification system's REST API.
URLs are automatically generated using DRF's DefaultRouter.

API Endpoints:
    - /api/notifications/
        - GET: List all notifications
        - POST: Create a new notification
    - /api/notifications/{id}/
        - GET: Retrieve a specific notification
        - PUT/PATCH: Update a notification
        - DELETE: Delete a notification
    - /api/notifications/mark_all_read/
        - POST: Mark all notifications as read
    - /api/preferences/
        - GET: Get user preferences
        - POST: Update user preferences
"""

# Create a router and register our viewsets
router = DefaultRouter()
router.register(
    r'notifications',
    views.NotificationsViewSet,
    basename='notification'
)
router.register(
    r'preferences',
    views.UserPreferencesViewSet,
    basename='preference'
)

# Wire up our API using automatic URL routing
urlpatterns = [
    path('api/', include(router.urls)),
]
