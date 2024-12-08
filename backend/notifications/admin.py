from django.contrib import admin
from .models import NotificationType, Notifications, UserPreferences

@admin.register(NotificationType)
class NotificationTypeAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for NotificationType model.
    
    Customizes how notification types are displayed and managed in the Django admin.
    
    Features:
        - List display shows key notification type information
        - Search capability across multiple fields
        - Ordering by name
    """
    
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Notifications model.
    
    Customizes how notifications are displayed and managed in the Django admin.
    
    Features:
        - List display shows key notification information
        - Search capability across multiple fields
        - Filtering by type, read status, priority, and dates
        - Read-only fields for created timestamp
    """
    
    list_display = ('recipient', 'notification_type', 'title', 'created_at', 'read', 'priority')
    list_filter = ('notification_type', 'read', 'priority', 'created_at')
    search_fields = ('title', 'message', 'recipient__username')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
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
    
    list_display = ('user', 'email_notifications', 'push_notifications')
    list_filter = ('email_notifications', 'push_notifications', 'enabled_types')
    search_fields = ('user__username',)
    filter_horizontal = ('enabled_types',)
    
    def get_queryset(self, request):
        """
        Optimizes database queries by prefetching related user data.
        
        Args:
            request: The HTTP request
            
        Returns:
            QuerySet with prefetched user data
        """
        return super().get_queryset(request).select_related('user')
