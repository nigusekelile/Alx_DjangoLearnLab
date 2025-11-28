"""
Unit tests for Django REST Framework API views.
Tests CRUD operations, filtering, searching, ordering, and permissions.
Uses self.client.login for authentication testing.
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
    Test CRUD operations for Book API views using self.client.login.
    """
    
    def test_book_list_view_unauthenticated(self):
        """
        Test that unauthenticated users can access book list.
        """
        url = reverse('api:book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
    
    def test_book_detail_view_unauthenticated(self):
        """
        Test that unauthenticated users can access book details.
        """
        url = reverse('api:book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
    
    def test_book_create_view_with_login(self):
        """
        Test that authenticated users can create books using self.client.login.
        """
        # Use self.client.login for authentication
        login_success = self.client.login(username='regular', password='testpass123')
        self.assertTrue(login_success, "Login should be successful")
        
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
        
        # Logout after test
        self.client.logout()
    
    def test_book_create_view_without_login(self):
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
    
    def test_book_update_view_with_login(self):
        """
        Test that authenticated users can update books using self.client.login.
        """
        # Use self.client.login for authentication
        login_success = self.client.login(username='regular', password='testpass123')
        self.assertTrue(login_success, "Login should be successful")
        
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
        
        # Logout after test
        self.client.logout()
    
    def test_book_update_view_without_login(self):
        """
        Test that unauthenticated users cannot update books.
        """
        url = reverse('api:book-update', kwargs={'pk': self.book1.id})
        update_data = {'title': 'Unauthorized Update'}
        response = self.client.put(url, update_data, format='json')
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_book_delete_view_with_login(self):
        """
        Test that authenticated users can delete books using self.client.login.
        """
        # Use self.client.login for authentication
        login_success = self.client.login(username='regular', password='testpass123')
        self.assertTrue(login_success, "Login should be successful")
        
        url = reverse('api:book-delete', kwargs={'pk': self.book1.id})
        book_title = self.book1.title
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(book_title, response.data['message'])
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())
        
        # Logout after test
        self.client.logout()
    
    def test_book_delete_view_without_login(self):
        """
        Test that unauthenticated users cannot delete books.
        """
        url = reverse('api:book-delete', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())
    
    def test_multiple_operations_with_same_login(self):
        """
        Test multiple operations with the same login session.
        """
        # Login once and perform multiple operations
        login_success = self.client.login(username='regular', password='testpass123')
        self.assertTrue(login_success, "Login should be successful")
        
        # Create a book
        create_url = reverse('api:book-create')
        book_data = {
            'title': 'Multiple Operations Book',
            'publication_year': 2022,
            'author': self.author1.id
        }
        create_response = self.client.post(create_url, book_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        
        # Get the new book ID
        new_book_id = create_response.data['book']['id']
        
        # Update the book
        update_url = reverse('api:book-update', kwargs={'pk': new_book_id})
        update_data = {'title': 'Updated Multiple Operations Book'}
        update_response = self.client.patch(update_url, update_data, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        
        # Delete the book
        delete_url = reverse('api:book-delete', kwargs={'pk': new_book_id})
        delete_response = self.client.delete(delete_url)
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        
        # Logout after all operations
        self.client.logout()


class BookViewFilteringTests(BaseAPITestCase):
    """
    Test filtering functionality in Book list view with authentication.
    """
    
    def test_filter_by_publication_year_with_login(self):
        """
        Test filtering books by publication year with authenticated user.
        """
        # Login first
        self.client.login(username='regular', password='testpass123')
        
        url = f"{reverse('api:book-list')}?publication_year=1997"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter and the Philosopher\'s Stone')
        
        self.client.logout()
    
    def test_filter_by_author_with_login(self):
        """
        Test filtering books by author ID with authenticated user.
        """
        # Login first
        self.client.login(username='regular', password='testpass123')
        
        url = f"{reverse('api:book-list')}?author={self.author2.id}"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 1984 and Animal Farm
        
        self.client.logout()
    
    def test_filter_by_author_name_with_login(self):
        """
        Test filtering books by author name with authenticated user.
        """
        # Login first
        self.client.login(username='regular', password='testpass123')
        
        url = f"{reverse('api:book-list')}?author_name=Rowling"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
        self.client.logout()


class BookViewSearchingTests(BaseAPITestCase):
    """
    Test searching functionality in Book list view with authentication.
    """
    
    def test_search_by_title_with_login(self):
        """
        Test searching books by title with authenticated user.
        """
        # Login first
        self.client.login(username='regular', password='testpass123')
        
        url = f"{reverse('api:book-list')}?search=Harry"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
        self.client.logout()
    
    def test_search_by_author_name_with_login(self):
        """
        Test searching books by author name with authenticated user.
        """
        # Login first
        self.client.login(username='regular', password='testpass123')
        
        url = f"{reverse('api:book-list')}?search=Orwell"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 1984 and Animal Farm
        
        self.client.logout()


class BookViewOrderingTests(BaseAPITestCase):
    """
    Test ordering functionality in Book list view with authentication.
    """
    
    def test_ordering_by_title_with_login(self):
        """
        Test ordering books by title with authenticated user.
        """
        # Login first
        self.client.login(username='regular', password='testpass123')
        
        url = f"{reverse('api:book-list')}?ordering=title"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))
        
        self.client.logout()
    
    def test_ordering_by_publication_year_with_login(self):
        """
        Test ordering books by publication year with authenticated user.
        """
        # Login first
        self.client.login(username='regular', password='testpass123')
        
        url = f"{reverse('api:book-list')}?ordering=-publication_year"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
        
        self.client.logout()


class AuthorViewTests(BaseAPITestCase):
    """
    Test Author API views with authentication.
    """
    
    def test_author_list_view_with_login(self):
        """
        Test that authenticated users can access author list.
        """
        # Login first
        self.client.login(username='regular', password='testpass123')
        
        url = reverse('api:author-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        
        self.client.logout()
    
    def test_author_detail_view_with_login(self):
        """
        Test that authenticated users can access author details.
        """
        # Login first
        self.client.login(username='regular', password='testpass123')
        
        url = reverse('api:author-detail', kwargs={'pk': self.author1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'J.K. Rowling')
        self.assertEqual(len(response.data['books']), 1)
        
        self.client.logout()


class ErrorHandlingViewTests(BaseAPITestCase):
    """
    Test error handling in API views with authentication.
    """
    
    def test_nonexistent_book_detail_with_login(self):
        """
        Test that authenticated users get 404 for non-existent books.
        """
        # Login first
        self.client.login(username='regular', password='testpass123')
        
        url = reverse('api:book-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        self.client.logout()
    
    def test_nonexistent_book_update_with_login(self):
        """
        Test that updating non-existent book returns 404 for authenticated users.
        """
        # Login first
        self.client.login(username='regular', password='testpass123')
        
        url = reverse('api:book-update', kwargs={'pk': 9999})
        update_data = {'title': 'Updated Title'}
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        self.client.logout()
    
    def test_create_book_invalid_data_with_login(self):
        """
        Test that creating book with invalid data returns 400 for authenticated users.
        """
        # Login first
        self.client.login(username='regular', password='testpass123')
        
        url = reverse('api:book-create')
        invalid_data = {
            'title': '',  # Empty title
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        self.client.logout()


class ValidationViewTests(BaseAPITestCase):
    """
    Test validation in API views with authentication.
    """
    
    def test_create_book_future_publication_year_with_login(self):
        """
        Test that creating book with future publication year returns validation error for authenticated users.
        """
        # Login first
        self.client.login(username='regular', password='testpass123')
        
        url = reverse('api:book-create')
        book_data = {
            'title': 'Future Book',
            'publication_year': 2030,  # Future year
            'author': self.author1.id
        }
        response = self.client.post(url, book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
        
        self.client.logout()
    
    def test_login_with_invalid_credentials(self):
        """
        Test that login fails with invalid credentials.
        """
        # Try to login with wrong password
        login_success = self.client.login(username='regular', password='wrongpassword')
        self.assertFalse(login_success, "Login should fail with wrong password")
        
        # Try to access protected endpoint
        url = reverse('api:book-create')
        book_data = {
            'title': 'Should Fail Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(url, book_data, format='json')
        
        # Should be unauthorized since login failed
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])


class AuthenticationFlowTests(BaseAPITestCase):
    """
    Test complete authentication flows with login and logout.
    """
    
    def test_complete_authentication_flow(self):
        """
        Test a complete flow: login → perform actions → logout → verify access denied.
        """
        # Step 1: Try to create book without login (should fail)
        url = reverse('api:book-create')
        book_data = {
            'title': 'Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response_before_login = self.client.post(url, book_data, format='json')
        self.assertIn(response_before_login.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        
        # Step 2: Login
        login_success = self.client.login(username='regular', password='testpass123')
        self.assertTrue(login_success, "Login should be successful")
        
        # Step 3: Create book after login (should succeed)
        response_after_login = self.client.post(url, book_data, format='json')
        self.assertEqual(response_after_login.status_code, status.HTTP_201_CREATED)
        
        # Step 4: Logout
        self.client.logout()
        
        # Step 5: Try to create another book after logout (should fail)
        another_book_data = {
            'title': 'Another Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response_after_logout = self.client.post(url, another_book_data, format='json')
        self.assertIn(response_after_logout.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])