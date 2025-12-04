from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase
import os

# Custom Tag model for additional functionality
class CustomTag(TagBase):
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('posts-by-tag', kwargs={'slug': self.slug})
    
    def get_post_count(self):
        """Return number of posts with this tag"""
        return self.tagged_items.count()
    
    @classmethod
    def get_popular_tags(cls, limit=10):
        """Get most popular tags based on post count"""
        return cls.objects.annotate(
            post_count=models.Count('tagged_items')
        ).order_by('-post_count')[:limit]

# Through model for custom tag relationships
class TaggedPost(GenericTaggedItemBase):
    tag = models.ForeignKey(
        CustomTag,
        on_delete=models.CASCADE,
        related_name="tagged_items"
    )

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Use TaggableManager from django-taggit
    tags = TaggableManager(
        through=TaggedPost,
        blank=True,
        verbose_name="Tags",
        help_text="Add tags separated by commas"
    )
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def get_update_url(self):
        return reverse('post-update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('post-delete', kwargs={'pk': self.pk})
    
    def get_short_content(self, length=150):
        """Return truncated content for preview"""
        if len(self.content) > length:
            return self.content[:length] + '...'
        return self.content
    
    def get_read_time(self):
        """Calculate approximate read time (assuming 200 words per minute)"""
        word_count = len(self.content.split())
        minutes = word_count / 200
        if minutes < 1:
            return "Less than a minute"
        elif minutes < 2:
            return "1 minute"
        else:
            return f"{int(minutes)} minutes"
    
    def comment_count(self):
        """Return the number of comments for this post"""
        return self.comments.count()
    
    def get_related_posts(self, limit=3):
        """Get related posts based on tags"""
        # Get posts with similar tags, excluding current post
        similar_posts = Post.objects.filter(
            tags__in=self.tags.all()
        ).exclude(pk=self.pk).distinct()
        
        # If not enough similar posts, get recent posts by same author
        if similar_posts.count() < limit:
            author_posts = Post.objects.filter(
                author=self.author
            ).exclude(pk=self.pk).distinct()
            similar_posts = list(similar_posts) + list(author_posts)
        
        return similar_posts[:limit]
    
    class Meta:
        ordering = ['-published_date']

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    def get_absolute_url(self):
        return self.post.get_absolute_url() + f'#comment-{self.pk}'
    
    def get_edit_url(self):
        return reverse('comment-edit', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('comment-delete', kwargs={'pk': self.pk})
    
    def can_edit(self, user):
        """Check if user can edit this comment"""
        return user.is_authenticated and (user == self.author or user.is_staff)
    
    def can_delete(self, user):
        """Check if user can delete this comment"""
        return user.is_authenticated and (user == self.author or user.is_staff)
    
    def get_time_since_created(self):
        """Get human-readable time since comment was created"""
        time_diff = timezone.now() - self.created_at
        
        if time_diff.days > 365:
            years = time_diff.days // 365
            return f"{years} year{'s' if years > 1 else ''} ago"
        elif time_diff.days > 30:
            months = time_diff.days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        elif time_diff.days > 0:
            return f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
        elif time_diff.seconds > 3600:
            hours = time_diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif time_diff.seconds > 60:
            minutes = time_diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "just now"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    @property
    def profile_picture_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return '/static/images/default_profile.png'
    
    def save(self, *args, **kwargs):
        try:
            old = Profile.objects.get(pk=self.pk)
            if old.profile_picture and old.profile_picture != self.profile_picture:
                if os.path.isfile(old.profile_picture.path):
                    os.remove(old.profile_picture.path)
        except Profile.DoesNotExist:
            pass
        super().save(*args, **kwargs)

# Signal to create/update profile when User is created/updated
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()