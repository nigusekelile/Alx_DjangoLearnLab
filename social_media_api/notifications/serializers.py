from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Notification, NotificationSettings


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for notifications."""
    actor = serializers.SerializerMethodField()
    recipient = serializers.SerializerMethodField()
    target_url = serializers.SerializerMethodField()
    time_since = serializers.ReadOnlyField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'actor', 'recipient', 'verb', 'message',
            'target_content_type', 'target_object_id',
            'is_read', 'created_at', 'time_since', 'target_url'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_actor(self, obj):
        """Get actor user info."""
        User = get_user_model()
        return {
            'id': obj.actor.id,
            'username': obj.actor.username,
            'profile_picture': obj.actor.profile_picture.url if obj.actor.profile_picture else None
        }
    
    def get_recipient(self, obj):
        """Get recipient user info."""
        User = get_user_model()
        return {
            'id': obj.recipient.id,
            'username': obj.recipient.username
        }
    
    def get_target_url(self, obj):
        """Get URL to the target object if applicable."""
        if obj.target:
            # Return appropriate URL based on target type
            if hasattr(obj.target, 'get_absolute_url'):
                return obj.target.get_absolute_url()
        return None


class NotificationSettingsSerializer(serializers.ModelSerializer):
    """Serializer for notification settings."""
    class Meta:
        model = NotificationSettings
        fields = [
            'email_follow', 'email_like', 'email_comment', 'email_mention',
            'app_follow', 'app_like', 'app_comment', 'app_mention', 'app_system'
        ]