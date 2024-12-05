from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class NotificationType(models.TextChoices):
    """
    Enumerates the different types of notifications that can be sent.
    
    Each notification type has a unique identifier and a human-readable name.
    """
    TASK_UPDATED = 'TASK_UPDATED', 'Task Updated'
    TASK_ASSIGNED = 'TASK_ASSIGNED', 'Task Assigned'
    TASK_COMPLETED = 'TASK_COMPLETED', 'Task Completed'

class Notifications(models.Model):
    """
    Represents a notification entity in the system.
    
    This model stores all notifications sent to users, including their status and metadata.
    Each notification is associated with a specific recipient user.
    
    Attributes:
        recipient (ForeignKey): The User who will receive this notification
        notification_type (str): Category/type of notification (e.g., 'TASK_UPDATED', 'TASK_ASSIGNED', 'TASK_COMPLETED')
        title (str): Short heading/subject of the notification
        message (str): Detailed content of the notification
        read (bool): Indicates if the notification has been read by the recipient
        created_at (datetime): Timestamp when notification was created
        updated_at (datetime): Timestamp when notification was last updated
    """
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text="User who will receive this notification"
    )
    notification_type = models.CharField(
        max_length=50,
        choices=NotificationType.choices,
        help_text="Category/type of notification (e.g., 'TASK_UPDATED', 'TASK_ASSIGNED', 'TASK_COMPLETED')"
    )
    title = models.CharField(
        max_length=255,
        help_text="Short heading/subject of the notification"
    )
    message = models.TextField(
        help_text="Detailed content of the notification"
    )
    read = models.BooleanField(
        default=False,
        help_text="Indicates if the notification has been read by the recipient"
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
        Meta configuration for Notifications model.
        Ensures proper plural name in Django admin and sets default ordering.
        """
        ordering = ['-created_at']  # Most recent notifications first
        verbose_name_plural = 'notifications'

    def __str__(self):
        """String representation of the notification"""
        return f"{self.notification_type} - {self.title}"

class UserPreferences(models.Model):
    """
    Stores user-specific notification preferences.
    
    This model maintains each user's notification preferences, allowing them to
    customize how they receive different types of notifications.
    
    Attributes:
        user (OneToOneField): The User whose preferences these are
        task_updated (bool): Whether user wants to receive notifications for task updates
        task_assigned (bool): Whether user wants to receive notifications for task assignments
        task_completed (bool): Whether user wants to receive notifications for task completions
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='notification_preferences',
        help_text="User whose preferences these are"
    )
    task_updated = models.BooleanField(
        default=True,
        help_text="Whether user wants to receive notifications for task updates"
    )
    task_assigned = models.BooleanField(
        default=True,
        help_text="Whether user wants to receive notifications for task assignments"
    )
    task_completed = models.BooleanField(
        default=True,
        help_text="Whether user wants to receive notifications for task completions"
    )

    class Meta:
        """
        Meta configuration for UserPreferences model.
        Ensures proper plural name in Django admin.
        """
        verbose_name_plural = 'user preferences'

    def __str__(self):
        """String representation of the user preferences"""
        return f"Preferences for {self.user.username}"
