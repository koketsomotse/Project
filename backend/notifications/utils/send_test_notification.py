import os
import django
import sys
import json
import asyncio
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import datetime
import random

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notification_system.settings')
django.setup()

from django.contrib.auth.models import User
from notifications.models import Notifications, NotificationType

def send_test_notification(username="Bret", notification_type=None):
    """
    Send a test notification to a specific user.
    
    Args:
        username (str): Username to send notification to
        notification_type (str): Type of notification to send (optional)
    """
    try:
        # Get the user
        user = User.objects.get(username=username)
        
        # Get random notification type if not specified
        if not notification_type:
            notification_type = random.choice([choice[0] for choice in NotificationType.choices])
        
        # Create notification content based on type
        if notification_type == "TASK_UPDATED":
            title = "Task Update: Project Review"
            message = "The project review task has been updated with new requirements."
        elif notification_type == "TASK_ASSIGNED":
            title = "New Task Assignment: Code Review"
            message = "You have been assigned to review the latest code changes."
        else:  # TASK_COMPLETED
            title = "Task Completed: Documentation"
            message = "The documentation task has been marked as complete."
        
        # Create notification in database
        notification = Notifications.objects.create(
            recipient=user,
            notification_type=notification_type,
            title=title,
            message=message
        )
        
        # Prepare notification data
        notification_data = {
            'id': notification.id,
            'title': notification.title,
            'message': notification.message,
            'notification_type': notification.notification_type,
            'created_at': notification.created_at.isoformat(),
            'read': notification.read
        }
        
        # Get channel layer and send notification
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}_notifications",
            {
                'type': 'notification_message',
                'message': notification_data
            }
        )
        
        print(f"\nNotification sent to {username}:")
        print(f"Type: {notification_type}")
        print(f"Title: {title}")
        print(f"Message: {message}\n")
        
        return True
        
    except User.DoesNotExist:
        print(f"Error: User '{username}' not found.")
        return False
    except Exception as e:
        print(f"Error sending notification: {str(e)}")
        return False

if __name__ == "__main__":
    # Get username and notification type from command line args
    username = sys.argv[1] if len(sys.argv) > 1 else "Bret"
    notification_type = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Send the test notification
    send_test_notification(username, notification_type)
