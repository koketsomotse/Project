import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from notifications.models import Notifications, NotificationType, UserPreferences
from channels.testing import WebsocketCommunicator
from notifications.consumers import NotificationsConsumer
from channels.db import database_sync_to_async
from faker import Faker
import json
import asyncio
from datetime import datetime, timedelta
from notification_system.routing import application

fake = Faker()

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
class TestNotificationE2E:
    @pytest.fixture
    async def setup_test_data(self):
        """Generate test users and notifications"""
        # Create test users
        users = []
        for _ in range(5):
            user = await database_sync_to_async(User.objects.create_user)(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password()
            )
            token = await database_sync_to_async(Token.objects.create)(user=user)
            users.append((user, token))

        # Create notification types
        notification_types = []
        types = ['TASK_CREATED', 'TASK_UPDATED', 'COMMENT_ADDED', 'MENTION', 'DEADLINE']
        for type_name in types:
            nt = await database_sync_to_async(NotificationType.objects.create)(
                name=type_name,
                description=f"Test notification for {type_name.lower()}"
            )
            notification_types.append(nt)

        # Generate notifications for each user
        notifications = []
        for user, _ in users:
            # Create user preferences
            await database_sync_to_async(UserPreferences.objects.create)(
                user=user,
                email_notifications=True,
                push_notifications=True
            )
            
            for _ in range(10):
                notif_type = fake.random_element(notification_types)
                notification = await database_sync_to_async(Notifications.objects.create)(
                    recipient=user,
                    title=fake.sentence(),
                    message=fake.paragraph(),
                    notification_type=notif_type,
                    created_at=fake.date_time_between(
                        start_date='-30d',
                        end_date='now'
                    )
                )
                notifications.append(notification)

        return {
            'users': users,
            'notification_types': notification_types,
            'notifications': notifications
        }

    async def test_notification_flow(self, setup_test_data):
        """Test the complete notification flow"""
        test_data = await setup_test_data
        user, token = test_data['users'][0]

        # Connect to WebSocket with token
        communicator = WebsocketCommunicator(
            application,
            f"ws/notifications/?token={token.key}"
        )
        connected, _ = await communicator.connect()
        assert connected, "WebSocket connection failed"

        # Create a new notification
        notification_type = test_data['notification_types'][0]
        new_notification = await database_sync_to_async(Notifications.objects.create)(
            recipient=user,
            title="Real-time Test",
            message="Testing real-time notification delivery",
            notification_type=notification_type
        )

        # Wait for real-time notification
        response = await communicator.receive_json_from()
        assert response['type'] == 'notification_message'
        assert 'message' in response
        assert response['message']['id'] == new_notification.id

        await communicator.disconnect()

    async def test_notification_filtering(self, setup_test_data):
        """Test notification filtering and pagination"""
        test_data = await setup_test_data
        user, token = test_data['users'][0]

        # Test API endpoint for filtered notifications
        from rest_framework.test import APIClient
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        # Test date range filtering
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        response = await database_sync_to_async(client.get)(
            '/api/notifications/',
            {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'page': 1
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        # Test type filtering
        notif_type = test_data['notification_types'][0]
        response = await database_sync_to_async(client.get)(
            '/api/notifications/',
            {'type': notif_type.name}
        )
        
        assert response.status_code == 200
        data = response.json()
        filtered_notifications = [n for n in data if n['notification_type']['name'] == notif_type.name]
        assert len(filtered_notifications) > 0

    async def test_notification_preferences(self, setup_test_data):
        """Test user notification preferences"""
        test_data = await setup_test_data
        user, token = test_data['users'][0]

        from rest_framework.test import APIClient
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        # Update notification preferences
        preferences = {
            'email_notifications': True,
            'push_notifications': False,
            'notification_types': [nt.id for nt in test_data['notification_types'][:2]]
        }

        response = await database_sync_to_async(client.post)(
            '/api/preferences/',
            preferences
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['email_notifications'] == preferences['email_notifications']
        assert data['push_notifications'] == preferences['push_notifications']
