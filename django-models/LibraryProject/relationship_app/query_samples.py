# relationship_app/query_samples.py
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.test import Client
from relationship_app.models import Author, Book, Library

def test_views():
    """Test the views using Django test client"""
    client = Client()
    
    print("Testing Function-based View (All Books):")
    response = client.get('/relationship/books/')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✓ Books view working!")
    
    print("\nTesting Class-based View (Library List):")
    response = client.get('/relationship/libraries/')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✓ Library list view working!")
    
    print("\nTesting Class-based View (Library Detail):")
    # Get first library to test detail view
    library = Library.objects.first()
    if library:
        response = client.get(f'/relationship/library/{library.pk}/')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✓ Library detail view working for {library.name}!")

if __name__ == "__main__":
    test_views()
