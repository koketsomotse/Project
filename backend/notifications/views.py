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

class NotificationsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user notifications.
    
    This ViewSet provides CRUD operations for notifications and additional
    actions like marking notifications as read and sending real-time updates.
    
    Attributes:
        queryset: QuerySet of all notifications
        serializer_class: Serializer class for notifications
        permission_classes: List of permission classes (requires authentication)
    """
    serializer_class = NotificationsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Get the list of notifications for the current user.
        
        Filters notifications to only show those belonging to the current user.
        Orders by creation date, with newest first.
        
        Returns:
            QuerySet: Filtered notifications for the current user
        """
        return Notifications.objects.filter(recipient=self.request.user)

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
        notifications = self.get_queryset().filter(read=False)
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

    def create(self, request, *args, **kwargs):
        """
        Create a new notification.
        
        Custom create method that checks user preferences before creating a notification.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: HTTP response with created notification data
        """
        # Add the recipient
        request.data['recipient'] = request.user.id
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
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
        
        self.perform_create(serializer)

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

    def perform_create(self, serializer):
        """
        Create a new notification.
        
        Sets the recipient as the current user.
        
        Args:
            serializer: The notification serializer instance
        """
        serializer.save(recipient=self.request.user)

class UserPreferencesViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user notification preferences.
    
    This ViewSet provides CRUD operations for user preferences and ensures
    each user can only access and modify their own preferences.
    
    Attributes:
        serializer_class: Serializer class for user preferences
        permission_classes: List of permission classes (requires authentication)
    """
    serializer_class = UserPreferencesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Get the preferences for the current user.
        
        Returns:
            QuerySet: Filtered preferences for the current user
        """
        return UserPreferences.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Create user preferences.
        
        Sets the user as the current user and ensures only one
        preference object exists per user.
        
        Args:
            serializer: The preference serializer instance
            
        Raises:
            ValidationError: If preferences already exist for the user
        """
        # Check if preferences already exist
        if UserPreferences.objects.filter(user=self.request.user).exists():
            return Response(
                {'detail': 'Preferences already exist. Use PUT to update.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create user preferences.
        
        Custom create method that checks if preferences already exist.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: HTTP response with created preference data
        """
        # Check if preferences already exist
        if UserPreferences.objects.filter(user=request.user).exists():
            return Response(
                {'detail': 'Preferences already exist. Use PUT to update.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)
