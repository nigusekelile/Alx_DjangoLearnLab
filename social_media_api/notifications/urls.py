from django.urls import path
from .views import (
    NotificationListView,
    UnreadNotificationListView,
    MarkNotificationAsReadView,
    MarkAllNotificationsAsReadView,
    NotificationCountView,
    NotificationSettingsView
)

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification_list'),
    path('unread/', UnreadNotificationListView.as_view(), name='unread_notifications'),
    path('<int:notification_id>/read/', MarkNotificationAsReadView.as_view(), name='mark_notification_read'),
    path('mark-all-read/', MarkAllNotificationsAsReadView.as_view(), name='mark_all_notifications_read'),
    path('count/', NotificationCountView.as_view(), name='notification_count'),
    path('settings/', NotificationSettingsView.as_view(), name='notification_settings'),
]