# relationship_app/management/commands/assign_permissions.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book, UserProfile

class Command(BaseCommand):
    help = 'Assign permissions to user roles'

    def handle(self, *args, **options):
        # Get content type for Book model
        content_type = ContentType.objects.get_for_model(Book)
        
        # Get all permissions for Book model
        can_add = Permission.objects.get(codename='can_add_book', content_type=content_type)
        can_change = Permission.objects.get(codename='can_change_book', content_type=content_type)
        can_delete = Permission.objects.get(codename='can_delete_book', content_type=content_type)
        can_view = Permission.objects.get(codename='can_view_book', content_type=content_type)
        
        # Assign permissions based on roles
        for profile in UserProfile.objects.all():
            user = profile.user
            user.user_permissions.clear()  # Clear existing permissions
            
            if profile.role == 'Admin':
                # Admins get all permissions
                user.user_permissions.add(can_add, can_change, can_delete, can_view)
                self.stdout.write(f"✅ Admin permissions assigned to {user.username}")
            
            elif profile.role == 'Librarian':
                # Librarians can add, change, and view books
                user.user_permissions.add(can_add, can_change, can_view)
                self.stdout.write(f"✅ Librarian permissions assigned to {user.username}")
            
            elif profile.role == 'Member':
                # Members can only view books
                user.user_permissions.add(can_view)
                self.stdout.write(f"✅ Member permissions assigned to {user.username}")
        
        self.stdout.write(self.style.SUCCESS('Successfully assigned permissions to all users!'))
