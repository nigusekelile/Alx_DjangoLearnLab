"""
Comprehensive testing script for filtering, searching, and ordering features.
Tests all advanced query capabilities of the Book API.
"""

import os
import django
import requests
from django.test import TestCase, Client
from django.contrib.auth.models import User
from api.models import Author, Book

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

def test_filtering_features():
    """Test all filtering, searching, and ordering features"""
    base_url = "http://127.0.0.1:8000/api/books"
    client = Client()
    
    print("🧪 Testing Filtering, Searching, and Ordering Features")
    print("=" * 60)
    
    # Create test data
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    
    books_data = [
        {'title': 'Harry Potter and the Philosopher\'s Stone', 'publication_year': 1997, 'author': author1},
        {'title': 'Harry Potter and the Chamber of Secrets', 'publication_year': 1998, 'author': author1},
        {'title': '1984', 'publication_year': 1949, 'author': author2},
        {'title': 'Animal Farm', 'publication_year': 1945, 'author': author2},
        {'title': 'The Hobbit', 'publication_year': 1937, 'author': Author.objects.create(name="J.R.R. Tolkien")},
    ]
    
    for book_data in books_data:
        Book.objects.create(**book_data)
    
    print("✅ Test data created")
    
    # Test 1: Basic filtering by publication year
    print("\n1. Testing exact year filtering:")
    response = client.get(f'{base_url}/?publication_year=1997')
    data = response.json()
    print(f"   URL: /api/books/?publication_year=1997")
    print(f"   Results: {len(data)} books")
    assert len(data) == 1, f"Expected 1 book, got {len(data)}"
    assert data[0]['title'] == "Harry Potter and the Philosopher's Stone"
    print("   ✅ Exact year filtering works")
    
    # Test 2: Range filtering
    print("\n2. Testing range filtering:")
    response = client.get(f'{base_url}/?publication_year_min=1990&publication_year_max=2000')
    data = response.json()
    print(f"   URL: /api/books/?publication_year_min=1990&publication_year_max=2000")
    print(f"   Results: {len(data)} books")
    assert len(data) == 2, f"Expected 2 books, got {len(data)}"
    print("   ✅ Range filtering works")
    
    # Test 3: Title contains filtering
    print("\n3. Testing title contains filtering:")
    response = client.get(f'{base_url}/?title=Harry')
    data = response.json()
    print(f"   URL: /api/books/?title=Harry")
    print(f"   Results: {len(data)} books")
    assert len(data) == 2, f"Expected 2 books, got {len(data)}"
    print("   ✅ Title contains filtering works")
    
    # Test 4: Author name filtering
    print("\n4. Testing author name filtering:")
    response = client.get(f'{base_url}/?author_name=Orwell')
    data = response.json()
    print(f"   URL: /api/books/?author_name=Orwell")
    print(f"   Results: {len(data)} books")
    assert len(data) == 2, f"Expected 2 books, got {len(data)}"
    print("   ✅ Author name filtering works")
    
    # Test 5: Combined search
    print("\n5. Testing combined search:")
    response = client.get(f'{base_url}/?search=Harry')
    data = response.json()
    print(f"   URL: /api/books/?search=Harry")
    print(f"   Results: {len(data)} books")
    assert len(data) == 2, f"Expected 2 books, got {len(data)}"
    print("   ✅ Combined search works")
    
    # Test 6: Ordering
    print("\n6. Testing ordering:")
    response = client.get(f'{base_url}/?ordering=-publication_year')
    data = response.json()
    print(f"   URL: /api/books/?ordering=-publication_year")
    print(f"   First book year: {data[0]['publication_year']}")
    assert data[0]['publication_year'] == 1998, "Ordering not working"
    print("   ✅ Descending ordering works")
    
    # Test 7: Multiple ordering
    print("\n7. Testing multiple field ordering:")
    response = client.get(f'{base_url}/?ordering=author__name,publication_year')
    data = response.json()
    print(f"   URL: /api/books/?ordering=author__name,publication_year")
    print(f"   Results: {len(data)} books")
    print("   ✅ Multiple field ordering works")
    
    # Test 8: Search with DRF SearchFilter
    print("\n8. Testing DRF SearchFilter:")
    response = client.get(f'{base_url}/?search=Animal')
    data = response.json()
    print(f"   URL: /api/books/?search=Animal')
    print(f"   Results: {len(data)} books")
    assert len(data) == 1, f"Expected 1 book, got {len(data)}"
    assert data[0]['title'] == 'Animal Farm'
    print("   ✅ DRF SearchFilter works")
    
    print("\n" + "=" * 60)
    print("🎉 All filtering, searching, and ordering tests passed!")
    print("\nAvailable query parameters:")
    print("  Filtering:")
    print("    publication_year, publication_year_min, publication_year_max")
    print("    title, title_exact, author, author_name")
    print("    search (combined title and author search)")
    print("  Ordering:")
    print("    ordering=field (ascending)")
    print("    ordering=-field (descending)")
    print("    Multiple: ordering=field1,-field2")

if __name__ == '__main__':
    test_filtering_features()
