# LibraryProject/bookshelf/management/commands/setup_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import CustomUser

class Command(BaseCommand):
    help = 'Creates default groups and assigns permissions'

    def handle(self, *args, **options):
        # Get content type for CustomUser model
        content_type = ContentType.objects.get_for_model(CustomUser)
        
        # Get permissions
        can_view = Permission.objects.get(codename='can_view', content_type=content_type)
        can_create = Permission.objects.get(codename='can_create', content_type=content_type)
        can_edit = Permission.objects.get(codename='can_edit', content_type=content_type)
        can_delete = Permission.objects.get(codename='can_delete', content_type=content_type)
        
        # Create Viewers group with view permission
        viewers, created = Group.objects.get_or_create(name='Viewers')
        viewers.permissions.add(can_view)
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created Viewers group'))
        
        # Create Editors group with view, create, and edit permissions
        editors, created = Group.objects.get_or_create(name='Editors')
        editors.permissions.add(can_view, can_create, can_edit)
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created Editors group'))
        
        # Create Admins group with all permissions
        admins, created = Group.objects.get_or_create(name='Admins')
        admins.permissions.add(can_view, can_create, can_edit, can_delete)
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created Admins group'))
        
        self.stdout.write(self.style.SUCCESS('Successfully set up all groups and permissions'))
