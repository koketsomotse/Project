from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notifications, UserPreferences
from .serializers import NotificationsSerializer, UserPreferencesSerializer

# Create your views here.

class NotificationsViewSet(viewsets.ViewSet):
    """
    ViewSet for managing user notifications.
    
    Provides endpoints for creating, retrieving, and managing notifications.
    All endpoints require user authentication.
    """
    
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        Creates a new notification for a user.
        
        - Validates the notification data
        - Checks user preferences before creating
        - Sends real-time update via WebSocket if created
        
        Returns:
            Response with created notification or error details
        """
        data = request.data.copy()
        data['recipient'] = request.user.id
        serializer = NotificationsSerializer(data=data)
        if serializer.is_valid():
            # Check if user has opted in for this notification type
            notification_type = serializer.validated_data['notification_type']
            preference_field = notification_type.lower()
            
            try:
                # Get user preferences or create default ones
                user_preference = UserPreferences.objects.get(user=request.user)
                if not getattr(user_preference, preference_field, True):
                    return Response(
                        {'detail': 'User has opted out of this notification type'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except UserPreferences.DoesNotExist:
                UserPreferences.objects.create(user=request.user)
            
            # Create the notification
            notification = serializer.save(recipient=request.user)
            
            # Send real-time notification via WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'user_{request.user.id}_notifications',
                {
                    'type': 'notification_message',
                    'message': NotificationsSerializer(notification).data
                }
            )
            
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def list(self, request):
        """
        Retrieves all notifications for the current user.
        
        Returns:
            Response containing a list of user's notifications
        """
        notifications = Notifications.objects.filter(recipient=request.user)
        serializer = NotificationsSerializer(notifications, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retrieves a specific notification.
        
        Args:
            pk: Primary key of the notification to retrieve
            
        Returns:
            Response containing the requested notification
        """
        notification = get_object_or_404(
            Notifications,
            pk=pk,
            recipient=request.user
        )
        serializer = NotificationsSerializer(notification)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """
        Marks a specific notification as read.
        
        Args:
            pk: Primary key of the notification to mark as read
            
        Returns:
            Response indicating success or failure
        """
        notification = get_object_or_404(
            Notifications,
            pk=pk,
            recipient=request.user
        )
        notification.read = True
        notification.save()
        return Response({'status': 'notification marked as read'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """
        Marks all notifications as read.
        
        Custom action that allows marking all notifications as read.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: HTTP response with success message
        """
        notifications = Notifications.objects.filter(recipient=request.user, read=False)
        notifications.update(read=True)
        return Response({'status': 'notifications marked as read'})

class UserPreferencesViewSet(viewsets.ViewSet):
    """
    ViewSet for managing user notification preferences.
    
    Provides endpoints for creating and retrieving user preferences
    for different types of notifications.
    """
    
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        Creates or updates user notification preferences.
        
        Returns:
            Response with created/updated preferences
        """
        try:
            # Try to get existing preferences
            preferences = UserPreferences.objects.get(user=request.user)
            serializer = UserPreferencesSerializer(preferences, data=request.data)
        except UserPreferences.DoesNotExist:
            # Create new preferences if none exist
            serializer = UserPreferencesSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request):
        """
        Retrieves the current user's notification preferences.
        
        Returns:
            Response containing user's preference settings
        """
        preferences = get_object_or_404(UserPreferences, user=request.user)
        serializer = UserPreferencesSerializer(preferences)
        return Response(serializer.data)
