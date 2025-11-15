# LibraryProject/bookshelf/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """Custom user manager for handling user creation with additional fields"""
    
    def create_user(self, email, username, date_of_birth, password=None, **extra_fields):
        """
        Create and return a regular user with an email, username, date of birth, and password.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        if not username:
            raise ValueError(_('The Username field must be set'))
        if not date_of_birth:
            raise ValueError(_('The Date of Birth field must be set'))
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            date_of_birth=date_of_birth,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, date_of_birth, password=None, **extra_fields):
        """
        Create and return a superuser with an email, username, date of birth, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, username, date_of_birth, password, **extra_fields)

class CustomUser(AbstractUser):
    """Custom user model with additional fields"""
    
    # Additional fields
    date_of_birth = models.DateField(_('date of birth'))
    profile_photo = models.ImageField(
        _('profile photo'), 
        upload_to='profile_photos/', 
        null=True, 
        blank=True,
        help_text=_('Upload a profile photo')
    )
    
    # Use email as the unique identifier instead of username
    email = models.EmailField(_('email address'), unique=True)
    
    # Additional fields for user profile
    bio = models.TextField(_('bio'), max_length=500, blank=True)
    phone_number = models.CharField(_('phone number'), max_length=15, blank=True)
    
    # Update the username field to be non-unique
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
    )
    
    # Set the custom manager
    objects = CustomUserManager()
    
    # Use email as the main identifier for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'date_of_birth']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'custom_user'
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Return the full name of the user"""
        return f"{self.first_name} {self.last_name}".strip() or self.username
