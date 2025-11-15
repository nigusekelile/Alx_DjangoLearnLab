# Create a simple migration script
# create_initial_migration.py
import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

try:
    django.setup()
    print("🔄 Creating initial migration for CustomUser...")
    
    # Create migration
    call_command('makemigrations', 'relationship_app', name='initial_customuser')
    
    print("✅ Initial migration created!")
    
except Exception as e:
    print(f"❌ Error: {e}")
