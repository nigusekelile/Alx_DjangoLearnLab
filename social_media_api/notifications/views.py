from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Notification, NotificationSettings
from .serializers import NotificationSerializer, NotificationSettingsSerializer
from .notify import NotificationManager


class StandardResultsSetPagination(PageNumberPagination):
    """Custom pagination class for notifications."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50


class NotificationListView(generics.ListAPIView):
    """View to list user's notifications."""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """Get notifications for the current user."""
        return Notification.objects.filter(recipient=self.request.user).select_related('actor', 'recipient')


class UnreadNotificationListView(generics.ListAPIView):
    """View to list user's unread notifications."""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get unread notifications for the current user."""
        return Notification.objects.filter(
            recipient=self.request.user,
            is_read=False
        ).select_related('actor', 'recipient').order_by('-created_at')


class MarkNotificationAsReadView(APIView):
    """View to mark a notification as read."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, notification_id):
        """Mark a specific notification as read."""
        notification = get_object_or_404(
            Notification,
            id=notification_id,
            recipient=request.user
        )
        notification.mark_as_read()
        
        return Response({
            'status': 'success',
            'message': 'Notification marked as read',
            'notification_id': notification_id
        })


class MarkAllNotificationsAsReadView(APIView):
    """View to mark all notifications as read."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Mark all notifications as read for the current user."""
        count = NotificationManager.mark_all_as_read(request.user)
        
        return Response({
            'status': 'success',
            'message': f'Marked {count} notifications as read',
            'count': count
        })


class NotificationCountView(APIView):
    """View to get count of unread notifications."""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get count of unread notifications."""
        count = NotificationManager.get_unread_count(request.user)
        
        return Response({
            'unread_count': count,
            'total_count': Notification.objects.filter(recipient=request.user).count()
        })


class NotificationSettingsView(generics.RetrieveUpdateAPIView):
    """View to get and update notification settings."""
    serializer_class = NotificationSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Get or create notification settings for the current user."""
        obj, created = NotificationSettings.objects.get_or_create(user=self.request.user)
        return obj