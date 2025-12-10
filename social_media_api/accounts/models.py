from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    """Custom user model with additional fields for social media."""
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        default='profile_pictures/default.png'
    )
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
    @property
    def followers_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.following.count()
    
    def follow(self, user):
        """Follow another user."""
        if user != self and not self.is_following(user):
            self.following.add(user)
            return True
        return False
    
    def unfollow(self, user):
        """Unfollow a user."""
        if user != self and self.is_following(user):
            self.following.remove(user)
            return True
        return False
    
    def is_following(self, user):
        """Check if current user is following the given user."""
        return self.following.filter(id=user.id).exists()
    
    def is_followed_by(self, user):
        """Check if current user is followed by the given user."""
        return self.followers.filter(id=user.id).exists()
    

class UserProfile(models.Model):
    """Extended profile information for users."""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='user_profile'
    )
    website = models.URLField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"