from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notifications, UserPreferences, NotificationType
from .serializers import NotificationsSerializer, UserPreferencesSerializer
from django.utils.dateparse import parse_datetime
from django.db.models import Q
from django.core.cache import cache

def get_user_notifications(user):
    # Always fetch fresh data from the database
    notifications = Notifications.objects.filter(recipient=user).order_by('-created_at')
    # Cache the notifications for 5 minutes
    cache.set(f'user_notifications_{user.id}', notifications, timeout=300)
    return notifications

class NotificationsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user notifications.
    """
    serializer_class = NotificationsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'is_read']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = get_user_notifications(self.request.user)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(
                created_at__range=[parse_datetime(start_date), parse_datetime(end_date)]
            )

        # Type filtering
        notif_type = self.request.query_params.get('type')
        if notif_type:
            queryset = queryset.filter(notification_type__name=notif_type)

        return queryset

    @action(detail=False, methods=['post'])
    def mark_read(self, request):
        notification_ids = request.data.get('notification_ids', [])
        if not notification_ids:
            return Response({'error': 'No notification IDs provided'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        notifications = Notifications.objects.filter(
            id__in=notification_ids,
            recipient=request.user
        )
        notifications.update(is_read=True)

        # Invalidate cache
        cache.delete(f'user_notifications_{request.user.id}')

        return Response({'status': 'notifications marked as read'})

    def perform_create(self, serializer):
        notification = serializer.save(recipient=self.request.user)
        # Invalidate cache for the user
        cache.delete(f'user_notifications_{notification.recipient.id}')
        # Send real-time notification via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'user_notifications_{notification.recipient.id}',
            {
                'type': 'new_notification',
                'notification': NotificationsSerializer(notification).data,
            }
        )
        return notification

    def perform_update(self, serializer):
        notification = serializer.save()
        # Invalidate cache for the user
        cache.delete(f'user_notifications_{notification.recipient.id}')
        return notification

    def perform_destroy(self, instance):
        recipient = instance.recipient
        instance.delete()
        # Invalidate cache for the user
        cache.delete(f'user_notifications_{recipient.id}')

class UserPreferencesViewSet(viewsets.ViewSet):
    """
    ViewSet for managing user notification preferences.
    """
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request):
        preferences, _ = UserPreferences.objects.get_or_create(
            user=request.user,
            defaults={
                'email_notifications': True,
                'push_notifications': True
            }
        )
        return Response(UserPreferencesSerializer(preferences).data)

    def create(self, request):
        preferences, _ = UserPreferences.objects.get_or_create(
            user=request.user
        )
        
        # Update preferences
        preferences.email_notifications = request.data.get(
            'email_notifications', preferences.email_notifications
        )
        preferences.push_notifications = request.data.get(
            'push_notifications', preferences.push_notifications
        )
        
        # Update notification types
        notification_types = request.data.get('notification_types', [])
        if notification_types:
            preferences.enabled_types.set(NotificationType.objects.filter(id__in=notification_types))
        
        preferences.save()
        return Response(UserPreferencesSerializer(preferences).data)
