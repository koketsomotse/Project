from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.db.models import Q
from .models import UserPreferences
from asgiref.sync import sync_to_async

class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.group_name = f'user_{self.user.id}_notifications'

        if self.user.is_authenticated:
            # Join group
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )

            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    async def notification_message(self, event):
        message = event['message']
        notification_type = message['notification_type']

        # Check user preferences before sending the notification
        user_preferences = await sync_to_async(UserPreferences.objects.get)(user=self.user)
        if notification_type == 'TASK_UPDATED' and not user_preferences.task_updated:
            return
        elif notification_type == 'TASK_ASSIGNED' and not user_preferences.task_assigned:
            return
        elif notification_type == 'TASK_COMPLETED' and not user_preferences.task_completed:
            return

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))