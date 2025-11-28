"""
Unit tests for Django REST Framework API views.
Tests CRUD operations, filtering, searching, ordering, and permissions.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Author, Book
from .serializers import BookSerializer, AuthorSerializer


class BaseAPITestCase(APITestCase):
    """
    Base test case with common setup methods for all API view tests.
    """
    
    def setUp(self):
        """
        Set up test data that will be used across multiple test cases.
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
        
        # Create API client
        self.client = APIClient()


class BookViewCRUDTests(BaseAPITestCase):
    """
    Test CRUD operations for Book API views.
    """
    
    def test_book_list_view(self):
        """
        Test that book list view returns all books with correct status code.
        """
        url = reverse('api:book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
    
    def test_book_detail_view(self):
        """
        Test that book detail view returns correct book data.
        """
        url = reverse('api:book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
        self.assertEqual(response.data['author'], self.author1.id)
    
    def test_book_create_view_authenticated(self):
        """
        Test that authenticated users can create books via create view.
        """
        self.client.force_authenticate(user=self.regular_user)
        
        url = reverse('api:book-create')
        book_data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(url, book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['book']['title'], 'New Test Book')
        self.assertTrue(Book.objects.filter(title='New Test Book').exists())
    
    def test_book_create_view_unauthenticated(self):
        """
        Test that unauthenticated users cannot create books.
        """
        url = reverse('api:book-create')
        book_data = {
            'title': 'Unauthorized Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(url, book_data, format='json')
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_book_update_view_authenticated(self):
        """
        Test that authenticated users can update books via update view.
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
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book Title')
    
    def test_book_update_view_unauthenticated(self):
        """
        Test that unauthenticated users cannot update books.
        """
        url = reverse('api:book-update', kwargs={'pk': self.book1.id})
        update_data = {'title': 'Unauthorized Update'}
        response = self.client.put(url, update_data, format='json')
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_book_delete_view_authenticated(self):
        """
        Test that authenticated users can delete books via delete view.
        """
        self.client.force_authenticate(user=self.regular_user)
        
        url = reverse('api:book-delete', kwargs={'pk': self.book1.id})
        book_title = self.book1.title
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(book_title, response.data['message'])
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())
    
    def test_book_delete_view_unauthenticated(self):
        """
        Test that unauthenticated users cannot delete books.
        """
        url = reverse('api:book-delete', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())


class BookViewFilteringTests(BaseAPITestCase):
    """
    Test filtering functionality in Book list view.
    """
    
    def test_filter_by_publication_year(self):
        """
        Test filtering books by publication year.
        """
        url = f"{reverse('api:book-list')}?publication_year=1997"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter and the Philosopher\'s Stone')
    
    def test_filter_by_author(self):
        """
        Test filtering books by author ID.
        """
        url = f"{reverse('api:book-list')}?author={self.author2.id}"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 1984 and Animal Farm
    
    def test_filter_by_author_name(self):
        """
        Test filtering books by author name.
        """
        url = f"{reverse('api:book-list')}?author_name=Rowling"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class BookViewSearchingTests(BaseAPITestCase):
    """
    Test searching functionality in Book list view.
    """
    
    def test_search_by_title(self):
        """
        Test searching books by title.
        """
        url = f"{reverse('api:book-list')}?search=Harry"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_search_by_author_name(self):
        """
        Test searching books by author name.
        """
        url = f"{reverse('api:book-list')}?search=Orwell"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 1984 and Animal Farm


class BookViewOrderingTests(BaseAPITestCase):
    """
    Test ordering functionality in Book list view.
    """
    
    def test_ordering_by_title_ascending(self):
        """
        Test ordering books by title in ascending order.
        """
        url = f"{reverse('api:book-list')}?ordering=title"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))
    
    def test_ordering_by_title_descending(self):
        """
        Test ordering books by title in descending order.
        """
        url = f"{reverse('api:book-list')}?ordering=-title"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))
    
    def test_ordering_by_publication_year_descending(self):
        """
        Test ordering books by publication year in descending order.
        """
        url = f"{reverse('api:book-list')}?ordering=-publication_year"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
    
    def test_ordering_by_author_name(self):
        """
        Test ordering books by author name.
        """
        url = f"{reverse('api:book-list')}?ordering=author__name"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthorViewTests(BaseAPITestCase):
    """
    Test Author API views.
    """
    
    def test_author_list_view(self):
        """
        Test that author list view returns all authors.
        """
        url = reverse('api:author-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_author_detail_view(self):
        """
        Test that author detail view returns correct author data with books.
        """
        url = reverse('api:author-detail', kwargs={'pk': self.author1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'J.K. Rowling')
        self.assertEqual(len(response.data['books']), 1)


class ErrorHandlingViewTests(BaseAPITestCase):
    """
    Test error handling in API views.
    """
    
    def test_nonexistent_book_detail(self):
        """
        Test that requesting non-existent book returns 404.
        """
        url = reverse('api:book-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_nonexistent_book_update(self):
        """
        Test that updating non-existent book returns 404.
        """
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('api:book-update', kwargs={'pk': 9999})
        update_data = {'title': 'Updated Title'}
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_nonexistent_book_delete(self):
        """
        Test that deleting non-existent book returns 404.
        """
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('api:book-delete', kwargs={'pk': 9999})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_book_invalid_data(self):
        """
        Test that creating book with invalid data returns 400.
        """
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('api:book-create')
        invalid_data = {
            'title': '',  # Empty title
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ValidationViewTests(BaseAPITestCase):
    """
    Test validation in API views.
    """
    
    def test_create_book_future_publication_year(self):
        """
        Test that creating book with future publication year returns validation error.
        """
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('api:book-create')
        book_data = {
            'title': 'Future Book',
            'publication_year': 2030,  # Future year
            'author': self.author1.id
        }
        response = self.client.post(url, book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)