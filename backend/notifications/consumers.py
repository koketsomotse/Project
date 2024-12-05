"""
WebSocket consumer for handling real-time notification updates:
- Notifications fetching
- New notification alerts
- Read status updates

This consumer maintains a WebSocket connection with the client and handles
various notification-related events.
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Notifications, UserPreferences

class NotificationsConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time notifications.
    
    This consumer manages WebSocket connections for real-time notification delivery.
    It handles connection establishment, message processing, and group management
    for user-specific notification channels.
    """

    async def connect(self):
        """
        Handle WebSocket connection establishment.
        
        - Authenticates the user
        - Creates a user-specific notification group
        - Accepts the connection
        """
        # Get the user from the scope (set by authentication middleware)
        self.user = self.scope["user"]
        
        if not self.user.is_authenticated:
            # Reject connection if user is not authenticated
            await self.close()
            return

        # Create user-specific group name
        self.group_name = f"user_{self.user.id}_notifications"
        
        # Add this channel to the user's notification group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        """
        Handle WebSocket disconnection.
        
        Args:
            close_code: The code indicating why the connection was closed
        """
        if hasattr(self, 'group_name'):
            # Remove this channel from the user's notification group
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        """
        Handle incoming WebSocket messages.
        
        Processes messages received from the client, such as:
        - Marking notifications as read
        - Updating notification preferences
        
        Args:
            text_data (str): JSON string containing the message data
        """
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'mark_read':
                # Handle marking notification as read
                notification_id = data.get('notification_id')
                if notification_id:
                    await self.mark_notification_read(notification_id)
                    
            elif message_type == 'update_preferences':
                # Handle updating user preferences
                preferences = data.get('preferences', {})
                if preferences:
                    await self.update_user_preferences(preferences)
                    
        except json.JSONDecodeError:
            # Handle invalid JSON data
            await self.send(text_data=json.dumps({
                'error': 'Invalid message format'
            }))

    async def notification_message(self, event):
        """
        Handle outgoing notification messages.
        
        Sends notifications to the connected client.
        
        Args:
            event (dict): Contains the notification data to be sent
        """
        # Send notification to WebSocket
        await self.send(text_data=json.dumps(event['message']))

    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        """
        Mark a notification as read.
        
        Args:
            notification_id (int): ID of the notification to mark as read
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            notification = Notifications.objects.get(
                id=notification_id,
                recipient=self.user
            )
            notification.read = True
            notification.save()
            return True
        except Notifications.DoesNotExist:
            return False

    @database_sync_to_async
    def update_user_preferences(self, preferences):
        """
        Update user notification preferences.
        
        Args:
            preferences (dict): New preference settings
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            user_prefs, created = UserPreferences.objects.get_or_create(
                user=self.user
            )
            
            # Update each preference if provided
            if 'task_updated' in preferences:
                user_prefs.task_updated = preferences['task_updated']
            if 'task_assigned' in preferences:
                user_prefs.task_assigned = preferences['task_assigned']
            if 'task_completed' in preferences:
                user_prefs.task_completed = preferences['task_completed']
                
            user_prefs.save()
            return True
        except Exception:
            return False
