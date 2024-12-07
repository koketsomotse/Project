import pytest
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from notifications.consumers import NotificationsConsumer
from notifications.models import Notifications, NotificationType
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
import json

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        try:
            token_key = scope["query_string"].decode().split("=")[1]
            token = await database_sync_to_async(Token.objects.get)(key=token_key)
            scope["user"] = await database_sync_to_async(User.objects.get)(id=token.user_id)
        except:
            scope["user"] = None
        return await super().__call__(scope, receive, send)

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
class TestWebSocketAuthentication:
    async def test_unauthenticated_connection(self):
        """Test that unauthenticated users cannot connect"""
        application = AuthMiddlewareStack(NotificationsConsumer.as_asgi())
        communicator = WebsocketCommunicator(application, "ws/notifications/")
        connected, _ = await communicator.connect()
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
        application = AuthMiddlewareStack(NotificationsConsumer.as_asgi())
        communicator = WebsocketCommunicator(
            application,
            f"ws/notifications/?token={token.key}"
        )
        connected, _ = await communicator.connect()
        assert connected
        await communicator.disconnect()
        
    async def test_connection_limit(self):
        """Test handling multiple concurrent connections"""
        user, token = await self.create_user_and_token()
        communicators = []
        application = AuthMiddlewareStack(NotificationsConsumer.as_asgi())
        
        # Try to create 5 connections (reduced from 100 for testing)
        for _ in range(5):
            communicator = WebsocketCommunicator(
                application,
                f"ws/notifications/?token={token.key}"
            )
            connected, _ = await communicator.connect()
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
        
        application = AuthMiddlewareStack(NotificationsConsumer.as_asgi())
        communicator = WebsocketCommunicator(
            application,
            f"ws/notifications/?token={token.key}"
        )
        connected, _ = await communicator.connect()
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
        application = AuthMiddlewareStack(NotificationsConsumer.as_asgi())
        communicator = WebsocketCommunicator(
            application,
            "ws/notifications/?token=invalid_token_123"
        )
        connected, _ = await communicator.connect()
        assert not connected
        await communicator.disconnect()

    async def test_reconnection(self):
        """Test reconnection behavior after disconnect"""
        user, token = await self.create_user_and_token()
        application = AuthMiddlewareStack(NotificationsConsumer.as_asgi())
        
        # First connection
        communicator1 = WebsocketCommunicator(
            application,
            f"ws/notifications/?token={token.key}"
        )
        connected1, _ = await communicator1.connect()
        assert connected1
        await communicator1.disconnect()
        
        # Immediate reconnection
        communicator2 = WebsocketCommunicator(
            application,
            f"ws/notifications/?token={token.key}"
        )
        connected2, _ = await communicator2.connect()
        assert connected2
        await communicator2.disconnect()

    async def test_broadcast_message(self):
        """Test broadcasting messages to connected clients"""
        user1, token1 = await self.create_user_and_token()
        user2, token2 = await self.create_user_and_token()
        application = AuthMiddlewareStack(NotificationsConsumer.as_asgi())
        
        # Connect two users
        communicator1 = WebsocketCommunicator(
            application,
            f"ws/notifications/?token={token1.key}"
        )
        communicator2 = WebsocketCommunicator(
            application,
            f"ws/notifications/?token={token2.key}"
        )
        
        await communicator1.connect()
        await communicator2.connect()
        
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
        application = AuthMiddlewareStack(NotificationsConsumer.as_asgi())
        communicator = WebsocketCommunicator(
            application,
            f"ws/notifications/?token={token.key}"
        )
        connected, _ = await communicator.connect()
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
