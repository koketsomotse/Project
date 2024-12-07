from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from .models import Notifications, UserPreferences, NotificationType
from .consumers import NotificationsConsumer
from .routing import websocket_urlpatterns
import json

class NotificationsModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.notification = Notifications.objects.create(
            recipient=self.user,
            notification_type='TASK_UPDATED',
            title='Test Notification',
            message='This is a test notification'
        )

    def test_notification_creation(self):
        """Test that a notification can be created"""
        self.assertEqual(self.notification.recipient, self.user)
        self.assertEqual(self.notification.title, 'Test Notification')
        self.assertFalse(self.notification.read)

class NotificationsAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.notification_data = {
            'notification_type': 'TASK_UPDATED',
            'title': 'Test Notification',
            'message': 'This is a test notification'
        }

    def test_create_notification(self):
        """Test creating a notification via API"""
        response = self.client.post('/api/notifications/', self.notification_data)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Notifications.objects.count(), 1)

    def test_list_notifications(self):
        """Test listing notifications"""
        # Create some notifications
        Notifications.objects.create(
            recipient=self.user,
            notification_type='TASK_UPDATED',
            title='Test 1',
            message='Message 1'
        )
        Notifications.objects.create(
            recipient=self.user,
            notification_type='TASK_ASSIGNED',
            title='Test 2',
            message='Message 2'
        )

        response = self.client.get('/api/notifications/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_mark_notification_read(self):
        """Test marking a notification as read"""
        notification = Notifications.objects.create(
            recipient=self.user,
            notification_type='TASK_UPDATED',
            title='Test',
            message='Message'
        )
        response = self.client.post(f'/api/notifications/{notification.id}/mark_read/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notification.refresh_from_db()
        self.assertTrue(notification.read)

class UserPreferencesTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.preference_data = {
            'task_updated': True,
            'task_assigned': False,
            'task_completed': True
        }

    def test_create_preferences(self):
        """Test creating user preferences"""
        response = self.client.post('/api/preferences/', self.preference_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserPreferences.objects.count(), 1)
        pref = UserPreferences.objects.first()
        self.assertTrue(pref.task_updated)
        self.assertFalse(pref.task_assigned)
        self.assertTrue(pref.task_completed)

    def test_update_preferences(self):
        """Test updating user preferences"""
        # First create preferences
        pref = UserPreferences.objects.create(user=self.user, **self.preference_data)
        
        # Update preferences
        update_data = {
            'task_updated': False,
            'task_assigned': True,
            'task_completed': False
        }
        response = self.client.put(f'/api/preferences/{pref.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pref.refresh_from_db()
        self.assertFalse(pref.task_updated)
        self.assertTrue(pref.task_assigned)
        self.assertFalse(pref.task_completed)

    def test_duplicate_preferences(self):
        """Test that a user cannot create multiple preferences"""
        # Create initial preferences
        response1 = self.client.post('/api/preferences/', self.preference_data)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Try to create another preference for the same user
        response2 = self.client.post('/api/preferences/', self.preference_data)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserPreferences.objects.count(), 1)

class WebSocketTests(TestCase):
    async def test_websocket_connection(self):
        """Test WebSocket connection and message handling"""
        # Create application
        application = AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
        
        # Create communicator
        communicator = WebsocketCommunicator(
            application=application,
            path='/ws/notifications/'
        )
        
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        
        # Test sending message
        await communicator.send_json_to({
            'message': 'fetch_notifications'
        })
        
        # Test receiving response
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'notifications_list')
        
        # Close
        await communicator.disconnect()
