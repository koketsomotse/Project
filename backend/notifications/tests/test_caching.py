from django.test import TestCase
from django.core.cache import cache
from notifications.models import Notifications, NotificationType
from django.contrib.auth.models import User
from notifications.views import get_user_notifications

class NotificationCacheTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.notification_type = NotificationType.objects.create(
            name='Test Type',
            description='Test Description'
        )
        self.notification = Notifications.objects.create(
            recipient=self.user,
            notification_type=self.notification_type,
            title='Test Notification',
            message='This is a test notification.',
            priority='MEDIUM'
        )

    def test_cache_notifications(self):
        # Fetch notifications for the first time (should hit the database)
        notifications = get_user_notifications(self.user)
        self.assertEqual(len(notifications), 1)

        # Fetch notifications again (should hit the cache)
        notifications = get_user_notifications(self.user)
        self.assertEqual(len(notifications), 1)

        # Ensure the cache is set
        cached_notifications = cache.get(f'user_notifications_{self.user.id}')
        self.assertIsNotNone(cached_notifications)

    def test_cache_timeout(self):
        # Fetch notifications and cache them
        notifications = get_user_notifications(self.user)
        self.assertEqual(len(notifications), 1)

        # Manually delete the cache
        cache.delete(f'user_notifications_{self.user.id}')

        # Fetch notifications again (should hit the database)
        notifications = get_user_notifications(self.user)
        self.assertEqual(len(notifications), 1)

    def test_cache_invalidation_on_notification_creation(self):
        # Fetch notifications and cache them
        notifications = get_user_notifications(self.user)
        self.assertEqual(len(notifications), 1)

        # Create a new notification
        new_notification = Notifications.objects.create(
            recipient=self.user,
            notification_type=self.notification_type,
            title='New Test Notification',
            message='This is a new test notification.',
            priority='MEDIUM'
        )

        # Fetch notifications again (should hit the database and return the new notification)
        notifications = get_user_notifications(self.user)
        self.assertEqual(len(notifications), 2)

    def test_cache_invalidation_on_notification_update(self):
        # Fetch notifications and cache them
        notifications = get_user_notifications(self.user)
        self.assertEqual(len(notifications), 1)

        # Update the existing notification
        self.notification.title = 'Updated Test Notification'
        self.notification.save()

        # Fetch notifications again (should hit the database and return the updated notification)
        notifications = get_user_notifications(self.user)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0].title, 'Updated Test Notification')

    def test_cache_invalidation_on_notification_deletion(self):
        # Fetch notifications and cache them
        notifications = get_user_notifications(self.user)
        self.assertEqual(len(notifications), 1)

        # Delete the existing notification
        self.notification.delete()

        # Fetch notifications again (should hit the database and return no notifications)
        notifications = get_user_notifications(self.user)
        self.assertEqual(len(notifications), 0)
