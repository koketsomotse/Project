from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class NotificationType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Notifications(models.Model):
    """
    Represents a notification entity in the system.
    
    This model stores all notifications sent to users, including their status and metadata.
    Each notification is associated with a specific recipient user.
    
    Relationships:
        - One-to-Many with User model (recipient)
    
    Fields:
        recipient: Links to the User who receives the notification
        notification_type: The category of notification (from NotificationType)
        title: Brief description of the notification
        message: Detailed content of the notification
        read: Tracks if the notification has been viewed
        created_at: When the notification was created
        updated_at: When the notification was last modified
    """
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text="User who will receive this notification"
    )
    notification_type = models.ForeignKey(
        NotificationType,
        on_delete=models.CASCADE,
        help_text="Category of notification"
    )
    title = models.CharField(
        max_length=255,
        help_text="Brief heading of the notification"
    )
    message = models.TextField(
        help_text="Full content of the notification"
    )
    read = models.BooleanField(
        default=False,
        help_text="Indicates if the notification has been read"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when notification was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when notification was last updated"
    )

    class Meta:
        """
        Model metadata options
        """
        verbose_name_plural = 'notifications'
        ordering = ['-created_at']  # Most recent notifications first

    def __str__(self):
        """
        String representation of the notification
        Returns: A string containing the notification type and recipient
        """
        return f"{self.notification_type.name} for {self.recipient.username}"

class UserPreferences(models.Model):
    """
    Stores user-specific notification preferences.
    
    This model maintains each user's notification preferences, allowing them to
    customize how they receive different types of notifications.
    
    Relationships:
        - One-to-One with User model
    
    Fields:
        user: The User whose preferences these are
        task_updated: Preference for task update notifications
        task_assigned: Preference for task assignment notifications
        task_completed: Preference for task completion notifications
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='notification_preferences',
        help_text="User whose preferences these are"
    )
    task_updated = models.BooleanField(
        default=True,
        help_text="Whether to receive task update notifications"
    )
    task_assigned = models.BooleanField(
        default=True,
        help_text="Whether to receive task assignment notifications"
    )
    task_completed = models.BooleanField(
        default=True,
        help_text="Whether to receive task completion notifications"
    )

    class Meta:
        verbose_name_plural = 'user preferences'

    def __str__(self):
        """
        String representation of the user preferences
        Returns: A string containing the username
        """
        return f"Preferences for {self.user.username}"
