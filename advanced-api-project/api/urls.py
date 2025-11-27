"""
URL configuration for API application.
Defines endpoints for Book CRUD operations with all required URL patterns.
Includes: books/, books/create/, books/update/, books/delete/
"""

from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Book CRUD endpoints - All required URLs
    path('books/', views.BookListView.as_view(), name='book-list'),           # GET - List all books
    path('books/create/', views.BookCreateView.as_view(), name='book-create'), # POST - Create new book
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'), # GET - Retrieve single book
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'), # PUT/PATCH - Update book
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'), # DELETE - Delete book
    
    # Author endpoints (read-only)
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
]