# check_migrations.py
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

def check_migration_status():
    print("🔍 Checking Migration Status...")
    
    # Check if relationship_app is in INSTALLED_APPS
    from django.apps import apps
    if apps.is_installed('relationship_app'):
        print("✅ relationship_app is installed")
    else:
        print("❌ relationship_app is NOT installed")
        return
    
    # Check migration files
    import os
    migration_files = os.listdir('relationship_app/migrations')
    print(f"📁 Migration files: {migration_files}")
    
    # Check database tables
    with connection.cursor() as cursor:
        tables = connection.introspection.table_names()
        print(f"📊 Total tables in database: {len(tables)}")
        
        # Check for our specific tables
        required_tables = [
            'relationship_app_userprofile',
            'relationship_app_author',
            'relationship_app_book', 
            'relationship_app_library',
            'relationship_app_librarian',
        ]
        
        print("🔍 Checking required tables:")
        for table in required_tables:
            if table in tables:
                print(f"   ✅ {table}")
            else:
                print(f"   ❌ {table} - MISSING")
        
        # Show UserProfile table structure if it exists
        if 'relationship_app_userprofile' in tables:
            print("\n📋 UserProfile table structure:")
            cursor.execute("PRAGMA table_info(relationship_app_userprofile)")
            columns = cursor.fetchall()
            for col in columns:
                print(f"   - {col[1]} ({col[2]})")

if __name__ == "__main__":
    check_migration_status()
