# LibraryProject/relationship_app/models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from bookshelf.models import CustomUser  # Import from bookshelf

# UserProfile model
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    
    user = models.OneToOneField(
        CustomUser,  # Use CustomUser from bookshelf
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

# Signals
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Create UserProfile automatically when a new CustomUser is created"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when CustomUser is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()

# Other models (Author, Book, Library, Librarian) remain the same
class Author(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publication_year = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey(
        CustomUser,  # Use CustomUser from bookshelf
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='books_created'
    )
    updated_by = models.ForeignKey(
        CustomUser,  # Use CustomUser from bookshelf
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='books_updated'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
            ("can_view_book", "Can view book"),
        ]

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='libraries')
    
    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')
    
    def __str__(self):
        return self.name
