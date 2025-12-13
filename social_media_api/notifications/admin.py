from django.contrib import admin
from .models import Notification, NotificationSettings


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'actor', 'verb', 'is_read', 'created_at')
    list_filter = ('verb', 'is_read', 'created_at')
    search_fields = ('recipient__username', 'actor__username', 'message')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('recipient', 'actor', 'verb', 'message')
        }),
        ('Target', {
            'fields': ('target_content_type', 'target_object_id')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )


@admin.register(NotificationSettings)
class NotificationSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_follow', 'email_like', 'app_follow', 'app_like')
    list_filter = ('email_follow', 'email_like', 'app_follow', 'app_like')
    search_fields = ('user__username',)