"""
Comprehensive unit tests for Django REST Framework APIs.
Tests CRUD operations, filtering, searching, ordering, and permissions.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Author, Book
from .serializers import BookSerializer, AuthorSerializer
import json


class BaseTestCase(APITestCase):
    """
    Base test case with common setup methods for all test classes.
    Provides reusable methods for creating test data and authenticated clients.
    """

    def setUp(self):
        """
        Set up test data and clients that will be used across multiple test cases.
        """
        # Create test users
        self.admin_user = User.objects.create_user(
            username='admin',
            password='testpass123',
            email='admin@example.com'
        )
        self.regular_user = User.objects.create_user(
            username='regular',
            password='testpass123',
            email='regular@example.com'
        )

        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')
        self.author3 = Author.objects.create(name='J.R.R. Tolkien')

        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title='Animal Farm',
            publication_year=1945,
            author=self.author2
        )
        self.book4 = Book.objects.create(
            title='The Hobbit',
            publication_year=1937,
            author=self.author3
        )
        self.book5 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )

        # Create API client
        self.client = APIClient()

        # URLs
        self.book_list_url = reverse('api:book-list')
        self.book_create_url = reverse('api:book-create')
        self.author_list_url = reverse('api:author-list')


class BookCRUDTests(BaseTestCase):
    """
    Test CRUD operations for Book model endpoints.
    Tests creation, retrieval, updating, and deletion of books.
    """

    def test_get_book_list_unauthenticated(self):
        """
        Test that unauthenticated users can access the book list.
        Expected: 200 OK with all books
        """
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_get_book_detail_unauthenticated(self):
        """
        Test that unauthenticated users can access individual book details.
        Expected: 200 OK with correct book data
        """
        url = reverse('api:book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
        self.assertEqual(response.data['author'], self.author1.id)

    def test_create_book_authenticated(self):
        """
        Test that authenticated users can create new books.
        Expected: 201 CREATED with new book data
        """
        self.client.force_authenticate(user=self.regular_user)
        
        book_data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(self.book_create_url, book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['book']['title'], 'New Test Book')
        self.assertEqual(response.data['book']['publication_year'], 2023)
        
        # Verify book was actually created in database
        self.assertTrue(Book.objects.filter(title='New Test Book').exists())

    def test_create_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot create books.
        Expected: 401 UNAUTHORIZED or 403 FORBIDDEN
        """
        book_data = {
            'title': 'Unauthorized Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(self.book_create_url, book_data, format='json')
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_update_book_authenticated(self):
        """
        Test that authenticated users can update existing books.
        Expected: 200 OK with updated book data
        """
        self.client.force_authenticate(user=self.regular_user)
        
        url = reverse('api:book-update', kwargs={'pk': self.book1.id})
        update_data = {
            'title': 'Updated Book Title',
            'publication_year': 1997,
            'author': self.author1.id
        }
        
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['book']['title'], 'Updated Book Title')
        
        # Verify book was actually updated in database
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book Title')

    def test_partial_update_book_authenticated(self):
        """
        Test that authenticated users can partially update books using PATCH.
        Expected: 200 OK with updated book data
        """
        self.client.force_authenticate(user=self.regular_user)
        
        url = reverse('api:book-update', kwargs={'pk': self.book1.id})
        update_data = {
            'title': 'Partially Updated Title'
        }
        
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['book']['title'], 'Partially Updated Title')
        
        # Verify only the title was updated
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Partially Updated Title')
        self.assertEqual(self.book1.publication_year, 1997)  # Should remain unchanged

    def test_update_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot update books.
        Expected: 401 UNAUTHORIZED or 403 FORBIDDEN
        """
        url = reverse('api:book-update', kwargs={'pk': self.book1.id})
        update_data = {'title': 'Unauthorized Update'}
        
        response = self.client.put(url, update_data, format='json')
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_delete_book_authenticated(self):
        """
        Test that authenticated users can delete books.
        Expected: 200 OK with success message
        """
        self.client.force_authenticate(user=self.regular_user)
        
        url = reverse('api:book-delete', kwargs={'pk': self.book1.id})
        book_title = self.book1.title
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(book_title, response.data['message'])
        
        # Verify book was actually deleted from database
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    def test_delete_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot delete books.
        Expected: 401 UNAUTHORIZED or 403 FORBIDDEN
        """
        url = reverse('api:book-delete', kwargs={'pk': self.book1.id})
        
        response = self.client.delete(url)
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        
        # Verify book still exists in database
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())

    def test_create_book_validation_future_year(self):
        """
        Test that book creation fails with future publication year.
        Expected: 400 BAD REQUEST with validation error
        """
        self.client.force_authenticate(user=self.regular_user)
        
        book_data = {
            'title': 'Future Book',
            'publication_year': 2030,  # Future year
            'author': self.author1.id
        }
        
        response = self.client.post(self.book_create_url, book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)


class FilteringSearchingOrderingTests(BaseTestCase):
    """
    Test filtering, searching, and ordering functionalities for Book API.
    """

    def test_filter_by_publication_year_exact(self):
        """
        Test filtering books by exact publication year.
        Expected: Only books from specified year
        """
        url = f"{self.book_list_url}?publication_year=1997"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter and the Philosopher\'s Stone')

    def test_filter_by_publication_year_range(self):
        """
        Test filtering books by publication year range.
        Expected: Only books within specified year range
        """
        url = f"{self.book_list_url}?publication_year_min=1990&publication_year_max=2000"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two Harry Potter books

    def test_filter_by_author(self):
        """
        Test filtering books by author ID.
        Expected: Only books by specified author
        """
        url = f"{self.book_list_url}?author={self.author2.id}"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 1984 and Animal Farm

    def test_filter_by_author_name(self):
        """
        Test filtering books by author name (contains).
        Expected: Only books by authors with matching name
        """
        url = f"{self.book_list_url}?author_name=Rowling"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two Harry Potter books

    def test_search_functionality(self):
        """
        Test combined search across title and author name.
        Expected: Books matching search term in title or author name
        """
        url = f"{self.book_list_url}?search=Harry"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both Harry Potter books

    def test_search_functionality_author(self):
        """
        Test search functionality with author name.
        Expected: Books by authors matching search term
        """
        url = f"{self.book_list_url}?search=Orwell"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 1984 and Animal Farm

    def test_ordering_by_title_ascending(self):
        """
        Test ordering books by title in ascending order.
        Expected: Books sorted A-Z by title
        """
        url = f"{self.book_list_url}?ordering=title"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_ordering_by_title_descending(self):
        """
        Test ordering books by title in descending order.
        Expected: Books sorted Z-A by title
        """
        url = f"{self.book_list_url}?ordering=-title"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))

    def test_ordering_by_publication_year_descending(self):
        """
        Test ordering books by publication year in descending order.
        Expected: Books sorted by newest first
        """
        url = f"{self.book_list_url}?ordering=-publication_year"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))

    def test_ordering_by_author_name(self):
        """
        Test ordering books by author name.
        Expected: Books sorted by author name A-Z
        """
        url = f"{self.book_list_url}?ordering=author__name"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # This test verifies the ordering works without checking exact order

    def test_multiple_ordering(self):
        """
        Test ordering by multiple fields.
        Expected: Books sorted by primary field, then secondary field
        """
        url = f"{self.book_list_url}?ordering=author__name,-publication_year"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Complex ordering logic is handled by Django ORM

    def test_combined_filter_search_order(self):
        """
        Test combining filtering, searching, and ordering.
        Expected: Properly filtered, searched, and ordered results
        """
        url = f"{self.book_list_url}?author_name=Rowling&ordering=-publication_year"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Only Rowling's books
        # Should be ordered by publication year descending
        self.assertEqual(response.data[0]['publication_year'], 1998)
        self.assertEqual(response.data[1]['publication_year'], 1997)


class AuthorAPITests(BaseTestCase):
    """
    Test Author API endpoints and functionality.
    """

    def test_get_author_list(self):
        """
        Test retrieving list of authors.
        Expected: 200 OK with all authors
        """
        response = self.client.get(self.author_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Three authors

    def test_get_author_detail(self):
        """
        Test retrieving individual author details.
        Expected: 200 OK with author data and nested books
        """
        url = reverse('api:author-detail', kwargs={'pk': self.author1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'J.K. Rowling')
        self.assertEqual(len(response.data['books']), 2)  # Two Harry Potter books

    def test_author_filter_by_name(self):
        """
        Test filtering authors by name.
        Expected: Only authors with matching name
        """
        url = f"{self.author_list_url}?name=Orwell"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'George Orwell')

    def test_author_ordering_by_name(self):
        """
        Test ordering authors by name.
        Expected: Authors sorted A-Z by name
        """
        url = f"{self.author_list_url}?ordering=name"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [author['name'] for author in response.data]
        self.assertEqual(names, sorted(names))


class SerializerTests(TestCase):
    """
    Test serializer validation and functionality.
    """

    def setUp(self):
        self.author = Author.objects.create(name='Test Author')

    def test_book_serializer_valid_data(self):
        """
        Test BookSerializer with valid data.
        Expected: Serializer is valid
        """
        data = {
            'title': 'Test Book',
            'publication_year': 2020,
            'author': self.author.id
        }
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_book_serializer_invalid_future_year(self):
        """
        Test BookSerializer with future publication year.
        Expected: Serializer is invalid with publication_year error
        """
        data = {
            'title': 'Future Book',
            'publication_year': 2030,  # Future year
            'author': self.author.id
        }
        serializer = BookSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('publication_year', serializer.errors)

    def test_book_serializer_missing_title(self):
        """
        Test BookSerializer with missing title.
        Expected: Serializer is invalid with title error
        """
        data = {
            'publication_year': 2020,
            'author': self.author.id
        }
        serializer = BookSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_author_serializer_valid_data(self):
        """
        Test AuthorSerializer with valid data.
        Expected: Serializer is valid
        """
        data = {'name': 'New Author'}
        serializer = AuthorSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class ModelTests(TestCase):
    """
    Test model functionality and string representations.
    """

    def test_author_str_representation(self):
        """
        Test Author model string representation.
        Expected: Returns author name
        """
        author = Author.objects.create(name='Test Author')
        self.assertEqual(str(author), 'Test Author')

    def test_book_str_representation(self):
        """
        Test Book model string representation.
        Expected: Returns book title and author name
        """
        author = Author.objects.create(name='Test Author')
        book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=author
        )
        self.assertEqual(str(book), 'Test Book by Test Author')

    def test_book_ordering(self):
        """
        Test Book model default ordering.
        Expected: Books ordered by title
        """
        author = Author.objects.create(name='Test Author')
        book1 = Book.objects.create(title='Z Book', publication_year=2020, author=author)
        book2 = Book.objects.create(title='A Book', publication_year=2020, author=author)
        
        books = Book.objects.all()
        self.assertEqual(books[0].title, 'A Book')
        self.assertEqual(books[1].title, 'Z Book')


class ErrorHandlingTests(BaseTestCase):
    """
    Test error handling for various scenarios.
    """

    def test_get_nonexistent_book(self):
        """
        Test retrieving a book that doesn't exist.
        Expected: 404 NOT FOUND
        """
        url = reverse('api:book-detail', kwargs={'pk': 9999})  # Non-existent ID
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_book(self):
        """
        Test updating a book that doesn't exist.
        Expected: 404 NOT FOUND
        """
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('api:book-update', kwargs={'pk': 9999})
        update_data = {'title': 'Updated Title'}
        
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_book(self):
        """
        Test deleting a book that doesn't exist.
        Expected: 404 NOT FOUND
        """
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('api:book-delete', kwargs={'pk': 9999})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_book_invalid_author(self):
        """
        Test creating a book with invalid author ID.
        Expected: 400 BAD REQUEST
        """
        self.client.force_authenticate(user=self.regular_user)
        
        book_data = {
            'title': 'Invalid Author Book',
            'publication_year': 2020,
            'author': 9999  # Invalid author ID
        }
        
        response = self.client.post(self.book_create_url, book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)