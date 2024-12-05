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
    A simple ViewSet for managing notifications.
    """
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        Create a new notification.
        
        Custom create method that checks user preferences before creating a notification.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: HTTP response with created notification data
        """
        serializer = NotificationsSerializer(data=request.data)
        if serializer.is_valid():
            # Add the recipient
            request.data['recipient'] = request.user.id
            
            # Check user preferences before creating notification
            notification_type = serializer.validated_data['notification_type']
            preference_field = notification_type.lower()
            
            try:
                user_preference = UserPreferences.objects.get(user=request.user)
                if not getattr(user_preference, preference_field, True):
                    return Response(
                        {'detail': 'User has opted out of this notification type'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except UserPreferences.DoesNotExist:
                # If no preferences exist, create default preferences
                UserPreferences.objects.create(user=request.user)
            
            notification = serializer.save()
            
            # Send real-time notification
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{request.user.id}_notifications",
                {
                    "type": "notification_message",
                    "message": serializer.data
                }
            )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
        Get the list of notifications for the current user.
        
        Filters notifications to only show those belonging to the current user.
        Orders by creation date, with newest first.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: HTTP response with notification data
        """
        user = request.user
        notifications = Notifications.objects.filter(recipient=user)
        return Response(NotificationsSerializer(notifications, many=True).data)

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """
        Mark all notifications as read.
        
        Custom action that allows marking all notifications as read.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: HTTP response with success message
        """
        notifications = Notifications.objects.filter(recipient=request.user, read=False)
        notifications.update(read=True)
        return Response({'status': 'notifications marked as read'})

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """
        Mark a notification as read.
        
        Custom action that allows marking a specific notification as read.
        
        Args:
            request: The HTTP request
            pk: Primary key of the notification
            
        Returns:
            Response: HTTP response with updated notification data
        """
        notification = get_object_or_404(Notifications, id=pk, recipient=request.user)
        notification.read = True
        notification.save()
        return Response({'status': 'notification marked as read'})

class UserPreferencesViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for managing user notification preferences.
    """

    def create(self, request):
        serializer = UserPreferencesSerializer(data=request.data)
        if serializer.is_valid():
            user_preferences, created = UserPreferences.objects.update_or_create(
                user=request.user,
                defaults=serializer.validated_data
            )
            return Response(UserPreferencesSerializer(user_preferences).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request):
        try:
            user_preferences = UserPreferences.objects.get(user=request.user)
            return Response(UserPreferencesSerializer(user_preferences).data)
        except UserPreferences.DoesNotExist:
            return Response({'detail': 'Preferences not found'}, status=status.HTTP_404_NOT_FOUND)
