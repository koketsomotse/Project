import pytest
from channels.testing import WebsocketCommunicator
from notifications.consumers import NotificationsConsumer
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestWebSocket:
    async def test_notification_delivery(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        communicator = WebsocketCommunicator(NotificationsConsumer.as_asgi(), 'ws://localhost:8000/ws/notifications/')
        connected, _ = await communicator.connect()
        assert connected
        
        # Simulate sending a notification
        await communicator.send_json_to({
            'type': 'send_notification',
            'message': 'New task assigned!'
        })
        response = await communicator.receive_json_from()
        assert response['message'] == 'New task assigned!'
        await communicator.disconnect()
