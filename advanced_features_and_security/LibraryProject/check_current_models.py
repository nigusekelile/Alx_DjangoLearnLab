# check_current_models.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

try:
    django.setup()
    from relationship_app.models import CustomUser
    print("✅ CustomUser model found!")
    print(f"Model name: {CustomUser.__name__}")
    print(f"DB table: {CustomUser._meta.db_table}")
except Exception as e:
    print(f"❌ Error: {e}")
