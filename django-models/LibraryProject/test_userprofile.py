# test_userprofile.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

def test_userprofile():
    print("🧪 Testing UserProfile functionality...")
    
    try:
        from django.contrib.auth.models import User
        from relationship_app.models import UserProfile
        
        # Create a test user
        user, created = User.objects.get_or_create(
            username='test_user',
            defaults={'email': 'test@example.com', 'password': 'testpass123'}
        )
        if created:
            user.set_password('testpass123')
            user.save()
            print("✅ Test user created")
        
        # Check if profile exists
        try:
            profile = user.profile
            print(f"✅ UserProfile exists: {user.username} -> {profile.role}")
        except UserProfile.DoesNotExist:
            print("❌ UserProfile does not exist for test user")
            # Try to create it manually
            profile = UserProfile.objects.create(user=user, role='Member')
            print(f"✅ UserProfile created manually: {profile}")
        
        # Test creating a new user to see if signal works
        new_user = User.objects.create_user('signal_test', 'signal@test.com', 'testpass123')
        print(f"✅ New user created: {new_user.username}")
        
        # Check if profile was automatically created
        try:
            new_profile = new_user.profile
            print(f"✅ Signal worked! Profile auto-created: {new_user.username} -> {new_profile.role}")
        except UserProfile.DoesNotExist:
            print("❌ Signal failed - no profile created")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_userprofile()
