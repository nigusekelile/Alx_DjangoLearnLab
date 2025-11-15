# setup_custom_user.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.core.management import call_command

def setup_custom_user_system():
    print("🚀 Setting up custom user model system...")
    
    # Step 1: Create migrations
    print("1. Creating migrations...")
    call_command('makemigrations', 'relationship_app')
    
    # Step 2: Apply migrations
    print("2. Applying migrations...")
    call_command('migrate')
    
    # Step 3: Create sample data
    print("3. Creating sample data...")
    call_command('populate_books')
    
    # Step 4: Setup permissions
    print("4. Setting up permissions...")
    call_command('setup_permissions')
    
    print("🎉 Custom user model system setup completed!")
    print("\n📝 Next steps:")
    print("   - Create a superuser: python manage.py createsuperuser")
    print("   - Run the server: python manage.py runserver")
    print("   - Access the admin: http://127.0.0.1:8000/admin/")

if __name__ == "__main__":
    setup_custom_user_system()
