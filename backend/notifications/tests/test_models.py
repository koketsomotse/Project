import pytest
from django.contrib.auth.models import User
from notifications.models import NotificationType, Notifications, UserPreferences
from django.core.exceptions import ValidationError
from django.utils import timezone

@pytest.mark.django_db
class TestNotificationsModel:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username='testuser',
            password='testpass'
        )

    @pytest.fixture
    def notification_type(self):
        return NotificationType.objects.create(
            name='TASK_ASSIGNED',
            description='A task has been assigned'
        )

    def test_create_notification(self, user, notification_type):
        """Test creating a notification with valid data"""
        notification = Notifications.objects.create(
            recipient=user,
            notification_type=notification_type,
            title='Test Notification',
            message='This is a test notification.',
            read=False,
            priority='MEDIUM'
        )
        assert notification.pk is not None
        assert notification.recipient == user
        assert notification.notification_type == notification_type
        assert notification.title == 'Test Notification'
        assert notification.read is False
        assert notification.priority == 'MEDIUM'
        assert notification.created_at is not None

    def test_notification_str_representation(self, user, notification_type):
        """Test string representation of notification"""
        notification = Notifications.objects.create(
            recipient=user,
            notification_type=notification_type,
            title='Test Notification',
            message='This is a test notification.',
            priority='HIGH'
        )
        expected_str = f"{notification_type}: Test Notification"
        assert str(notification) == expected_str

    def test_notification_ordering(self, user, notification_type):
        """Test notifications are ordered by created_at descending"""
        notification1 = Notifications.objects.create(
            recipient=user,
            notification_type=notification_type,
            title='First Notification',
            message='First test notification',
            priority='LOW'
        )
        notification2 = Notifications.objects.create(
            recipient=user,
            notification_type=notification_type,
            title='Second Notification',
            message='Second test notification',
            priority='MEDIUM'
        )
        notifications = Notifications.objects.all()
        assert notifications[0] == notification2
        assert notifications[1] == notification1

    def test_invalid_priority(self, user, notification_type):
        """Test that invalid priority raises validation error"""
        with pytest.raises(ValidationError):
            notification = Notifications.objects.create(
                recipient=user,
                notification_type=notification_type,
                title='Test Notification',
                message='Test notification',
                priority='INVALID'
            )
            notification.full_clean()

@pytest.mark.django_db
class TestUserPreferencesModel:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username='testuser',
            password='testpass'
        )

    @pytest.fixture
    def notification_types(self):
        types = [
            NotificationType.objects.create(
                name='TYPE1',
                description='First type'
            ),
            NotificationType.objects.create(
                name='TYPE2',
                description='Second type'
            )
        ]
        return types

    def test_create_user_preferences(self, user, notification_types):
        """Test creating user preferences with valid data"""
        preferences = UserPreferences.objects.create(
            user=user,
            email_notifications=True,
            push_notifications=True
        )
        preferences.enabled_types.set(notification_types)

        assert preferences.pk is not None
        assert preferences.user == user
        assert preferences.email_notifications is True
        assert preferences.push_notifications is True
        assert preferences.enabled_types.count() == 2
        assert list(preferences.enabled_types.all()) == notification_types

    def test_user_preferences_str(self, user):
        """Test string representation of user preferences"""
        preferences = UserPreferences.objects.create(
            user=user,
            email_notifications=True,
            push_notifications=False
        )
        expected_str = f"Preferences for {user.username}"
        assert str(preferences) == expected_str

    def test_unique_user_constraint(self, user):
        """Test that a user can only have one preferences record"""
        UserPreferences.objects.create(
            user=user,
            email_notifications=True,
            push_notifications=True
        )
        with pytest.raises(Exception):
            UserPreferences.objects.create(
                user=user,
                email_notifications=False,
                push_notifications=False
            )

    def test_enabled_types_empty(self, user):
        """Test that enabled_types can be empty"""
        preferences = UserPreferences.objects.create(
            user=user,
            email_notifications=True,
            push_notifications=True
        )
        assert preferences.enabled_types.count() == 0

@pytest.mark.django_db
class TestNotificationTypeModel:
    def test_create_notification_type(self):
        """Test creating a notification type"""
        notification_type = NotificationType.objects.create(
            name='TEST_TYPE',
            description='Test notification type'
        )
        assert notification_type.pk is not None
        assert notification_type.name == 'TEST_TYPE'
        assert notification_type.description == 'Test notification type'
        assert notification_type.created_at is not None
        assert notification_type.updated_at is not None

    def test_notification_type_str(self):
        """Test string representation of notification type"""
        notification_type = NotificationType.objects.create(
            name='TEST_TYPE',
            description='Test notification type'
        )
        assert str(notification_type) == 'TEST_TYPE'

    def test_unique_name_constraint(self):
        """Test that notification type names must be unique"""
        NotificationType.objects.create(
            name='UNIQUE_TYPE',
            description='First type'
        )
        with pytest.raises(Exception):
            NotificationType.objects.create(
                name='UNIQUE_TYPE',
                description='Second type with same name'
            )

    def test_name_max_length(self):
        """Test name field max length validation"""
        with pytest.raises(ValidationError):
            notification_type = NotificationType(
                name='A' * 51,  # Max length is 50
                description='Test type'
            )
            notification_type.full_clean()
