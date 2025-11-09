# test_authentication.py
import os
import django
from django.test import Client
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

def test_authentication():
    client = Client()
    
    print("Testing Authentication System")
    print("=" * 40)
    
    # Test registration
    print("\n1. Testing User Registration:")
    response = client.post('/relationship/register/', {
        'username': 'testuser',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
    })
    print(f"Registration status: {response.status_code}")
    
    # Test login
    print("\n2. Testing User Login:")
    response = client.post('/relationship/login/', {
        'username': 'testuser',
        'password': 'testpassword123',
    })
    print(f"Login status: {response.status_code}")
    
    # Test accessing protected views
    print("\n3. Testing Protected Views:")
    response = client.get('/relationship/books/')
    print(f"Books view status (after login): {response.status_code}")
    
    # Test logout
    print("\n4. Testing User Logout:")
    response = client.get('/relationship/logout/')
    print(f"Logout status: {response.status_code}")
    
    # Test accessing protected views after logout
    response = client.get('/relationship/books/')
    print(f"Books view status (after logout): {response.status_code}")
    print("(Should redirect to login)")
    
    print("\n✅ Authentication test completed!")

if __name__ == "__main__":
    test_authentication()
