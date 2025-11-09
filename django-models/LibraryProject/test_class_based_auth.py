# test_class_based_auth.py
import os
import django
from django.test import Client
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

def test_class_based_auth():
    client = Client()
    
    print("Testing Class-Based Authentication Views")
    print("=" * 50)
    
    # Test login page accessibility
    print("\n1. Testing LoginView:")
    response = client.get('/relationship/login/')
    print(f"Login page status: {response.status_code}")
    print(f"Using template: {response.template_name}")
    
    # Test logout page accessibility
    print("\n2. Testing LogoutView:")
    response = client.get('/relationship/logout/')
    print(f"Logout page status: {response.status_code}")
    print(f"Using template: {response.template_name}")
    
    # Test registration page
    print("\n3. Testing Registration:")
    response = client.get('/relationship/register/')
    print(f"Registration page status: {response.status_code}")
    
    # Test successful login
    print("\n4. Testing Login Functionality:")
    # Create a test user first
    user = User.objects.create_user('testuser2', 'test@example.com', 'testpass123')
    response = client.post('/relationship/login/', {
        'username': 'testuser2',
        'password': 'testpass123',
    })
    print(f"Login POST status: {response.status_code}")
    print(f"Redirected to: {getattr(response, 'url', 'No redirect')}")
    
    print("\n✅ Class-based authentication test completed!")

if __name__ == "__main__":
    test_class_based_auth()
