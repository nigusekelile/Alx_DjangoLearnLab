# verify_settings.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

try:
    django.setup()
    
    print("🔧 Checking Django settings...")
    
    # Check AUTH_USER_MODEL
    auth_user_model = getattr(settings, 'AUTH_USER_MODEL', None)
    print(f"AUTH_USER_MODEL: {auth_user_model}")
    
    if auth_user_model == 'bookshelf.CustomUser':
        print("✅ AUTH_USER_MODEL is correctly set to 'bookshelf.CustomUser'")
    else:
        print(f"❌ AUTH_USER_MODEL should be 'bookshelf.CustomUser', but is '{auth_user_model}'")
    
    # Check INSTALLED_APPS order
    installed_apps = getattr(settings, 'INSTALLED_APPS', [])
    print(f"INSTALLED_APPS: {installed_apps}")
    
    if 'bookshelf' in installed_apps and installed_apps.index('bookshelf') < installed_apps.index('django.contrib.auth'):
        print("✅ bookshelf is correctly placed before django.contrib.auth")
    else:
        print("❌ bookshelf must come before django.contrib.auth in INSTALLED_APPS")
    
    # Try to import the CustomUser model
    try:
        from bookshelf.models import CustomUser
        print("✅ CustomUser model can be imported from bookshelf")
        print(f"CustomUser fields: {[f.name for f in CustomUser._meta.fields]}")
    except ImportError as e:
        print(f"❌ Cannot import CustomUser from bookshelf: {e}")
        
except Exception as e:
    print(f"❌ Error during setup: {e}")
