# force_create_tables.py
import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

def force_create_tables():
    print("🔄 Forcing table creation...")
    
    try:
        # Create migrations
        print("1. Creating migrations...")
        call_command('makemigrations', 'relationship_app')
        
        # Apply migrations
        print("2. Applying migrations...")
        call_command('migrate', 'relationship_app')
        
        # Check if tables were created
        from django.db import connection
        with connection.cursor() as cursor:
            tables = connection.introspection.table_names()
            if 'relationship_app_userprofile' in tables:
                print("✅ SUCCESS: UserProfile table created!")
            else:
                print("❌ FAILED: UserProfile table still missing")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    force_create_tables()
