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
    
    Provides a secure way to serialize user data, excluding sensitive information.
    Only includes necessary fields for notification-related operations.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['username']  # Prevent username modifications through API


class NotificationsSerializer(serializers.ModelSerializer):
    """
    Serializer for Notifications model.
    
    Handles the conversion of Notification instances to/from JSON format.
    Includes additional validation and recipient user details.
    
    Fields:
        recipient: Nested UserSerializer for detailed user information
        created_at: Read-only field, automatically set
        updated_at: Read-only field, automatically updated
    """
    recipient = UserSerializer(read_only=True)
    
    class Meta:
        model = Notifications
        fields = [
            'id',
            'recipient',
            'notification_type',
            'title',
            'message',
            'read',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_notification_type(self, value):
        """
        Validate the notification_type field.
        
        Args:
            value (str): The notification type to validate
            
        Returns:
            str: The validated notification type
            
        Raises:
            serializers.ValidationError: If notification type is invalid
        """
        valid_types = [choice[0] for choice in self.Meta.model.NotificationType.choices]
        if value not in valid_types:
            raise serializers.ValidationError(
                f"Invalid notification type. Must be one of: {', '.join(valid_types)}"
            )
        return value


class UserPreferencesSerializer(serializers.ModelSerializer):
    """
    Serializer for UserPreferences model.
    
    Handles the conversion of UserPreferences instances to/from JSON format.
    Includes user details and preference validation.
    
    Fields:
        user: Nested UserSerializer for detailed user information
        All boolean preference fields
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserPreferences
        fields = [
            'id',
            'user',
            'task_updated',
            'task_assigned',
            'task_completed'
        ]

    def validate(self, data):
        """
        Validate the entire UserPreferences instance.
        
        Ensures that at least one notification type is enabled.
        
        Args:
            data (dict): The preference data to validate
            
        Returns:
            dict: The validated preference data
            
        Raises:
            serializers.ValidationError: If all preferences are disabled
        """
        if not any([
            data.get('task_updated', False),
            data.get('task_assigned', False),
            data.get('task_completed', False)
        ]):
            raise serializers.ValidationError(
                "At least one notification type must be enabled"
            )
        return data
