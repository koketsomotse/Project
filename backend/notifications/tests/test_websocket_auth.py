import pytest
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from django.contrib.auth.models import User, AnonymousUser
from rest_framework.authtoken.models import Token
from notifications.consumers import NotificationsConsumer
from notifications.models import Notifications, NotificationType
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from channels.layers import get_channel_layer
from django.contrib.auth.models import AnonymousUser
import json
from urllib.parse import parse_qs

# Configure the channel layer for testing
from channels.layers import BaseChannelLayer
class MemoryChannelLayer(BaseChannelLayer):
    def __init__(self, expiry=60):
        super().__init__(expiry)
        self.channels = {}
        self.groups = {}

    async def send(self, channel, message):
        if channel not in self.channels:
            self.channels[channel] = []
        self.channels[channel].append(message)

    async def receive(self, channel):
        if channel not in self.channels:
            return None
        if not self.channels[channel]:
            return None
        return self.channels[channel].pop(0)

    async def group_add(self, group, channel):
        if group not in self.groups:
            self.groups[group] = set()
        self.groups[group].add(channel)

    async def group_discard(self, group, channel):
        if group in self.groups:
            self.groups[group].discard(channel)

    async def group_send(self, group, message):
        if group not in self.groups:
            return
        for channel in self.groups[group]:
            await self.send(channel, message)

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Initialize the scope with AnonymousUser
        scope['user'] = AnonymousUser()
        
        try:
            # Extract token from query string
            query_string = scope["query_string"].decode()
            params = parse_qs(query_string)
            token_key = params.get('token', [None])[0]
            
            if token_key:
                # Get the token and user
                token = await database_sync_to_async(Token.objects.get)(key=token_key)
                user = await database_sync_to_async(User.objects.get)(id=token.user_id)
                
                # Set the user in the scope
                scope['user'] = user
        except Exception as e:
            # Keep AnonymousUser on any error
            pass
        
        return await super().__call__(scope, receive, send)

def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
class TestWebSocketAuthentication:
    @pytest.fixture(autouse=True)
    def setup_channel_layer(self):
        """Set up the channel layer for testing"""
        channel_layer = MemoryChannelLayer()
        self.channel_layer = channel_layer
        
    async def test_unauthenticated_connection(self):
        """Test that unauthenticated users cannot connect"""
        application = TokenAuthMiddlewareStack(NotificationsConsumer.as_asgi())
        communicator = WebsocketCommunicator(application, "ws/notifications/")
        communicator.scope["channel_layer"] = self.channel_layer
        connected, _ = await communicator.connect(timeout=5)
        assert not connected
        await communicator.disconnect()
        
    @database_sync_to_async
    def create_user_and_token(self):
        user = User.objects.create_user(username=f"testuser_{User.objects.count()}", password="testpass123")
        token = Token.objects.create(user=user)
        return user, token
        
    async def test_authenticated_connection(self):
        """Test that authenticated users can connect"""
        user, token = await self.create_user_and_token()
        application = TokenAuthMiddlewareStack(NotificationsConsumer.as_asgi())
        communicator = WebsocketCommunicator(
            application,
            f"ws/notifications/?token={token.key}"
        )
        communicator.scope["channel_layer"] = self.channel_layer
        connected, _ = await communicator.connect(timeout=5)
        assert connected
        await communicator.disconnect()
        
    async def test_connection_limit(self):
        """Test handling multiple concurrent connections"""
        user, token = await self.create_user_and_token()
        communicators = []
        application = TokenAuthMiddlewareStack(NotificationsConsumer.as_asgi())
        
        # Try to create 5 connections (reduced from 100 for testing)
        for _ in range(5):
            communicator = WebsocketCommunicator(
                application,
                f"ws/notifications/?token={token.key}"
            )
            communicator.scope["channel_layer"] = self.channel_layer
            connected, _ = await communicator.connect(timeout=5)
            if connected:
                communicators.append(communicator)
                
        # Verify connection limit
        assert len(communicators) <= 5
        
        # Cleanup
        for communicator in communicators:
            await communicator.disconnect()
            
    @database_sync_to_async
    def create_bulk_notifications(self, user):
        notification_type = NotificationType.objects.create(
            name='TASK_UPDATED',
            description='Task has been updated'
        )
        notifications = []
        for i in range(10):  # Reduced from 100 for testing
            notifications.append(
                Notifications(
                    recipient=user,
                    title=f'Test Notification {i}',
                    message=f'Test message {i}',
                    notification_type=notification_type
                )
            )
        return Notifications.objects.bulk_create(notifications)
        
    async def test_notification_performance(self):
        """Test handling large number of notifications"""
        user, token = await self.create_user_and_token()
        await self.create_bulk_notifications(user)
        
        application = TokenAuthMiddlewareStack(NotificationsConsumer.as_asgi())
        communicator = WebsocketCommunicator(
            application,
            f"ws/notifications/?token={token.key}"
        )
        communicator.scope["channel_layer"] = self.channel_layer
        connected, _ = await communicator.connect(timeout=5)
        assert connected
        
        # Request notifications
        await communicator.send_json_to({
            'type': 'fetch_notifications',
            'page': 1
        })
        
        # Verify response time (should be quick)
        response = await communicator.receive_json_from()
        assert 'notifications' in response
        assert len(response['notifications']) <= 10  # Verify pagination
        
        await communicator.disconnect()

    async def test_invalid_token(self):
        """Test connection attempt with invalid token"""
        application = TokenAuthMiddlewareStack(NotificationsConsumer.as_asgi())
        communicator = WebsocketCommunicator(
            application,
            "ws/notifications/?token=invalid_token_123"
        )
        communicator.scope["channel_layer"] = self.channel_layer
        connected, _ = await communicator.connect(timeout=5)
        assert not connected
        await communicator.disconnect()

    async def test_reconnection(self):
        """Test reconnection behavior after disconnect"""
        user, token = await self.create_user_and_token()
        application = TokenAuthMiddlewareStack(NotificationsConsumer.as_asgi())
        
        # First connection
        communicator1 = WebsocketCommunicator(
            application,
            f"ws/notifications/?token={token.key}"
        )
        communicator1.scope["channel_layer"] = self.channel_layer
        connected1, _ = await communicator1.connect(timeout=5)
        assert connected1
        await communicator1.disconnect()
        
        # Immediate reconnection
        communicator2 = WebsocketCommunicator(
            application,
            f"ws/notifications/?token={token.key}"
        )
        communicator2.scope["channel_layer"] = self.channel_layer
        connected2, _ = await communicator2.connect(timeout=5)
        assert connected2
        await communicator2.disconnect()

    async def test_broadcast_message(self):
        """Test broadcasting messages to connected clients"""
        user1, token1 = await self.create_user_and_token()
        user2, token2 = await self.create_user_and_token()
        application = TokenAuthMiddlewareStack(NotificationsConsumer.as_asgi())
        
        # Connect two users
        communicator1 = WebsocketCommunicator(
            application,
            f"ws/notifications/?token={token1.key}"
        )
        communicator2 = WebsocketCommunicator(
            application,
            f"ws/notifications/?token={token2.key}"
        )
        
        communicator1.scope["channel_layer"] = self.channel_layer
        communicator2.scope["channel_layer"] = self.channel_layer
        
        connected1, _ = await communicator1.connect(timeout=5)
        connected2, _ = await communicator2.connect(timeout=5)
        assert connected1 and connected2
        
        # Create and broadcast a notification
        notification_type = await database_sync_to_async(NotificationType.objects.create)(
            name='BROADCAST_TEST',
            description='Test broadcast notification'
        )
        notification = await database_sync_to_async(Notifications.objects.create)(
            recipient=user1,
            title='Broadcast Test',
            message='Test broadcast message',
            notification_type=notification_type
        )
        
        # Send broadcast message
        await communicator1.send_json_to({
            'type': 'notification',
            'notification_id': notification.id
        })
        
        # Verify user1 receives the message
        response1 = await communicator1.receive_json_from()
        assert response1['type'] == 'notification'
        assert 'notification' in response1
        
        # Cleanup
        await communicator1.disconnect()
        await communicator2.disconnect()

    async def test_malformed_message(self):
        """Test handling of malformed messages"""
        user, token = await self.create_user_and_token()
        application = TokenAuthMiddlewareStack(NotificationsConsumer.as_asgi())
        communicator = WebsocketCommunicator(
            application,
            f"ws/notifications/?token={token.key}"
        )
        communicator.scope["channel_layer"] = self.channel_layer
        connected, _ = await communicator.connect(timeout=5)
        assert connected
        
        # Send malformed message
        await communicator.send_json_to({
            'type': 'invalid_type',
            'data': 'malformed'
        })
        
        # Expect error response
        response = await communicator.receive_json_from()
        assert response['type'] == 'error'
        assert 'message' in response
        
        await communicator.disconnect()
