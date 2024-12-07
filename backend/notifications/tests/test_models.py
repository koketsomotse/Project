import pytest
from django.urls import reverse
from notifications.models import Notifications, UserPreferences
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestNotificationsModel:
    def test_create_notification(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        notification = Notifications.objects.create(
            recipient=user,
            notification_type='TASK_ASSIGNED',
            title='Test Notification',
            message='This is a test notification.',
            read=False
        )
        assert notification.recipient == user
        assert notification.title == 'Test Notification'
        assert notification.message == 'This is a test notification.'
        assert notification.read is False

class TestUserPreferencesModel:
    def test_create_user_preferences(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        preferences = UserPreferences.objects.create(
            user=user,
            task_updated=True,
            task_assigned=False,
            task_completed=True
        )
        assert preferences.user == user
        assert preferences.task_updated is True
        assert preferences.task_assigned is False
        assert preferences.task_completed is True
