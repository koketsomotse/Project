from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.db.models import Q
from .models import Notifications, UserPreferences
from .serializers import NotificationsSerializer
from asgiref.sync import sync_to_async
from django.core.paginator import Paginator

class NotificationsConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time notifications.
    """
    
    async def connect(self):
        """
        Handles new WebSocket connections.
        """
        self.user = self.scope['user']
        self.group_name = f"user_{self.user.id}"

        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        """
        Handles WebSocket disconnections.
        """
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive_json(self, content):
        """
        Handle incoming WebSocket messages.
        """
        message_type = content.get('type')
        
        if message_type == 'fetch_notifications':
            await self.fetch_notifications(content)
        elif message_type == 'mark_read':
            await self.mark_notifications_read(content)

    @sync_to_async
    def get_notifications(self, page=1):
        """
        Get paginated notifications for the current user.
        """
        notifications = Notifications.objects.filter(
            recipient=self.user
        ).order_by('-created_at')
        
        paginator = Paginator(notifications, 10)
        page_obj = paginator.get_page(page)
        
        return {
            'notifications': NotificationsSerializer(page_obj, many=True).data,
            'has_next': page_obj.has_next(),
            'total_pages': paginator.num_pages,
            'total_count': paginator.count
        }

    async def fetch_notifications(self, content):
        """
        Fetch notifications for the current user.
        """
        page = content.get('page', 1)
        notifications_data = await self.get_notifications(page)
        
        await self.send_json({
            'type': 'notifications_list',
            **notifications_data
        })

    async def notification_message(self, event):
        """
        Handles incoming notification messages from other parts of the application.
        """
        await self.send_json({
            'type': 'notification',
            'notification': event['notification']
        })

    @sync_to_async
    def mark_as_read(self, notification_ids):
        """
        Mark notifications as read.
        """
        Notifications.objects.filter(
            id__in=notification_ids,
            recipient=self.user
        ).update(is_read=True)

    async def mark_notifications_read(self, content):
        """
        Handle marking notifications as read.
        """
        notification_ids = content.get('notification_ids', [])
        if notification_ids:
            await self.mark_as_read(notification_ids)
            await self.send_json({
                'type': 'notifications_marked_read',
                'notification_ids': notification_ids
            })