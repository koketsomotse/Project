import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from notifications.models import UserPreferences, NotificationType
from rest_framework.test import APIClient
from rest_framework import status

@pytest.mark.django_db(transaction=True)
class TestNotificationPreferences(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a unique username for each test
        self.user = User.objects.create_user(
            username=f'testuser_{User.objects.count()}',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.notification_type = NotificationType.objects.create(
            name='TASK_UPDATED',
            description='Task has been updated'
        )
        
    def test_create_preferences(self):
        """Test creating notification preferences"""
        data = {
            'email_notifications': True,
            'push_notifications': True,
            'notification_types': [self.notification_type.id]
        }
        response = self.client.post('/api/preferences/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UserPreferences.objects.filter(user=self.user).exists())
        
    def test_update_preferences(self):
        """Test updating notification preferences"""
        # Create initial preferences
        preferences = UserPreferences.objects.create(
            user=self.user,
            email_notifications=True,
            push_notifications=True
        )
        preferences.notification_types.add(self.notification_type)
        
        # Update preferences
        data = {
            'email_notifications': False,
            'push_notifications': True,
            'notification_types': [self.notification_type.id]
        }
        response = self.client.put(f'/api/preferences/{preferences.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify changes
        preferences.refresh_from_db()
        self.assertFalse(preferences.email_notifications)
        self.assertTrue(preferences.push_notifications)
        
    def test_invalid_notification_type(self):
        """Test handling invalid notification type"""
        data = {
            'email_notifications': True,
            'push_notifications': True,
            'notification_types': [999]  # Invalid ID
        }
        response = self.client.post('/api/preferences/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_multiple_notification_types(self):
        """Test handling multiple notification types"""
        task_created = NotificationType.objects.create(
            name='TASK_CREATED',
            description='Task has been created'
        )
        data = {
            'email_notifications': True,
            'push_notifications': True,
            'notification_types': [self.notification_type.id, task_created.id]
        }
        response = self.client.post('/api/preferences/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        preferences = UserPreferences.objects.get(user=self.user)
        self.assertEqual(preferences.notification_types.count(), 2)
