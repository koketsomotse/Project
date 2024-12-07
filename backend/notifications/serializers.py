"""
Serializers for the notifications app.
This module defines how the model instances should be converted to and from JSON.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Notifications, UserPreferences

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    
    Handles serialization of user data, excluding sensitive information
    like passwords and only including necessary fields for notifications.
    """
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']  # Prevent id modifications through API

class NotificationsSerializer(serializers.ModelSerializer):
    """
    Serializer for Notifications model.
    
    Handles the conversion of Notification instances to/from JSON.
    Includes validation and custom field handling.
    
    Fields:
        - All fields from Notifications model
        - recipient: Nested UserSerializer for detailed user info
    """
    
    recipient = UserSerializer(read_only=True)
    
    class Meta:
        model = Notifications
        fields = [
            'id', 'recipient', 'notification_type',
            'title', 'message', 'read',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']  # Prevent id, created_at, and updated_at modifications through API

    def validate_notification_type(self, value):
        """
        Validates the notification type.
        
        Ensures the notification type is one of the predefined choices.
        
        Args:
            value: The notification type to validate
            
        Returns:
            The validated notification type
            
        Raises:
            serializers.ValidationError: If notification type is invalid
        """
        valid_types = ['TASK_UPDATED', 'TASK_ASSIGNED', 'TASK_COMPLETED']
        if value not in valid_types:
            raise serializers.ValidationError(
                f"Invalid notification type. Must be one of: {', '.join(valid_types)}"
            )
        return value

class UserPreferencesSerializer(serializers.ModelSerializer):
    """
    Serializer for UserPreferences model.
    
    Handles the conversion of UserPreferences instances to/from JSON.
    Includes the user's preferences for different notification types.
    """
    
    user = UserSerializer(read_only=True)  # Include user details
    
    class Meta:
        model = UserPreferences
        fields = [
            'id', 'user', 'task_updated',
            'task_assigned', 'task_completed'
        ]
        read_only_fields = ['id', 'user']  # Prevent id and user modifications through API

    def validate(self, data):
        """
        Validates the entire UserPreferences instance.
        
        Ensures at least one notification type is enabled to prevent
        users from completely disabling all notifications.
        
        Args:
            data: The preference data to validate
            
        Returns:
            The validated preference data
            
        Raises:
            serializers.ValidationError: If all preferences are disabled
        """
        if not any([
            data.get('task_updated', True),
            data.get('task_assigned', True),
            data.get('task_completed', True)
        ]):
            raise serializers.ValidationError(
                "At least one notification type must be enabled"
            )
        return data
