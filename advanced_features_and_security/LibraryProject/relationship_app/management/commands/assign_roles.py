# relationship_app/management/commands/assign_roles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from relationship_app.models import UserProfile

class Command(BaseCommand):
    help = 'Assign roles to existing users'

    def handle(self, *args, **options):
        # Get or create profiles for all users
        for user in User.objects.all():
            profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                # Assign default role 'Member' to new profiles
                profile.role = 'Member'
                profile.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Created profile for {user.username} with role Member')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully assigned roles to all users!')
        )
