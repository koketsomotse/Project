import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestNotificationViews:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_get_notifications(self):
        response = self.client.get(reverse('notification-list'))
        assert response.status_code == status.HTTP_200_OK

    def test_create_notification(self):
        data = {
            'recipient': self.user.id,
            'notification_type': 'TASK_ASSIGNED',
            'title': 'Test Notification',
            'message': 'This is a test notification.'
        }
        response = self.client.post(reverse('notification-list'), data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'Test Notification'
