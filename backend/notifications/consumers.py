from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.db.models import Q
from .models import UserPreferences
from asgiref.sync import sync_to_async

class NotificationsConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time notifications.
    
    This consumer manages WebSocket connections for each user,
    allowing them to receive notifications in real-time based
    on their preferences.
    """

    async def connect(self):
        """
        Handles new WebSocket connections.
        
        - Authenticates the user
        - Creates a unique group name for the user
        - Adds the user to their notification group if authenticated
        - Closes the connection if user is not authenticated
        """
        self.user = self.scope['user']
        self.group_name = f'user_{self.user.id}_notifications'

        if self.user.is_authenticated:
            # Add user to their notification group
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        """
        Handles WebSocket disconnection.
        
        Removes the user from their notification group when
        they disconnect from the WebSocket.
        
        Args:
            close_code: The code indicating why the connection was closed
        """
        # Remove user from their notification group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Handles incoming WebSocket messages.
        
        Currently not implemented as this is a one-way
        notification system (server to client only).
        
        Args:
            text_data: The message received from the client
        """
        pass

    async def notification_message(self, event):
        """
        Handles sending notifications to connected clients.
        
        Checks user preferences before sending any notification
        to ensure users only receive notifications they've opted into.
        
        Args:
            event: Dictionary containing the notification message and type
        """
        message = event['message']
        notification_type = message['notification_type']

        # Check user preferences before sending
        user_preferences = await sync_to_async(UserPreferences.objects.get)(user=self.user)
        
        # Only send notification if user has opted in for this type
        if notification_type == 'TASK_UPDATED' and not user_preferences.task_updated:
            return
        elif notification_type == 'TASK_ASSIGNED' and not user_preferences.task_assigned:
            return
        elif notification_type == 'TASK_COMPLETED' and not user_preferences.task_completed:
            return

        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))