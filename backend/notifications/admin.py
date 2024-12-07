from django.contrib import admin
from .models import Notifications, UserPreferences

@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Notifications model.
    
    Customizes how notifications are displayed and managed in the Django admin.
    
    Features:
        - List display shows key notification information
        - Search capability across multiple fields
        - Filtering by type, read status, and dates
        - Read-only fields for created/updated timestamps
    """
    
    list_display = [
        'id', 'recipient', 'notification_type',
        'title', 'read', 'created_at'
    ]
    list_filter = ['notification_type', 'read', 'created_at']
    search_fields = ['title', 'message', 'recipient__username']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        """
        Optimizes database queries by prefetching related recipient data.
        
        Args:
            request: The HTTP request
            
        Returns:
            QuerySet with prefetched recipient data
        """
        return super().get_queryset(request).select_related('recipient')

@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for UserPreferences model.
    
    Customizes how user preferences are displayed and managed in the Django admin.
    
    Features:
        - List display shows user and their notification preferences
        - Search by username
        - Filter by preference settings
    """
    
    list_display = [
        'user', 'task_updated', 'task_assigned',
        'task_completed'
    ]
    list_filter = [
        'task_updated', 'task_assigned',
        'task_completed'
    ]
    search_fields = ['user__username']
    
    def get_queryset(self, request):
        """
        Optimizes database queries by prefetching related user data.
        
        Args:
            request: The HTTP request
            
        Returns:
            QuerySet with prefetched user data
        """
        return super().get_queryset(request).select_related('user')
