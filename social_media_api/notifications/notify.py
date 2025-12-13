from django.contrib.contenttypes.models import ContentType
from .models import Notification, NotificationSettings


class NotificationManager:
    """Manager for creating and handling notifications."""
    
    @staticmethod
    def create_notification(recipient, actor, verb, target=None, message=None):
        """Create a notification for a user."""
        # Check if user wants this type of notification
        try:
            settings = recipient.notification_settings
            if verb == 'follow' and not settings.app_follow:
                return None
            elif verb == 'like' and not settings.app_like:
                return None
            elif verb == 'comment' and not settings.app_comment:
                return None
            elif verb == 'mention' and not settings.app_mention:
                return None
            elif verb == 'system' and not settings.app_system:
                return None
        except NotificationSettings.DoesNotExist:
            # Create default settings if they don't exist
            NotificationSettings.objects.create(user=recipient)
        
        # Generate default message if not provided
        if not message:
            if verb == 'follow':
                message = f"{actor.username} started following you"
            elif verb == 'like':
                message = f"{actor.username} liked your post"
            elif verb == 'comment':
                message = f"{actor.username} commented on your post"
            elif verb == 'mention':
                message = f"{actor.username} mentioned you in a post"
            elif verb == 'system':
                message = "System notification"
        
        # Create notification
        notification = Notification.objects.create(
            recipient=recipient,
            actor=actor,
            verb=verb,
            message=message
        )
        
        # Set target if provided
        if target:
            notification.target_content_type = ContentType.objects.get_for_model(target)
            notification.target_object_id = target.id
            notification.save()
        
        return notification
    
    @staticmethod
    def notify_follow(follower, followed_user):
        """Create notification for new follower."""
        return NotificationManager.create_notification(
            recipient=followed_user,
            actor=follower,
            verb='follow',
            message=f"{follower.username} started following you"
        )
    
    @staticmethod
    def notify_like(user, post):
        """Create notification for post like."""
        if user != post.author:  # Don't notify if user likes their own post
            return NotificationManager.create_notification(
                recipient=post.author,
                actor=user,
                verb='like',
                target=post,
                message=f"{user.username} liked your post: {post.title[:50]}..."
            )
        return None
    
    @staticmethod
    def notify_comment(user, comment):
        """Create notification for new comment."""
        if user != comment.post.author:  # Don't notify if user comments on their own post
            return NotificationManager.create_notification(
                recipient=comment.post.author,
                actor=user,
                verb='comment',
                target=comment,
                message=f"{user.username} commented on your post"
            )
        return None
    
    @staticmethod
    def mark_all_as_read(user):
        """Mark all notifications as read for a user."""
        return Notification.objects.filter(recipient=user, is_read=False).update(is_read=True)
    
    @staticmethod
    def get_unread_count(user):
        """Get count of unread notifications for a user."""
        return Notification.objects.filter(recipient=user, is_read=False).count()