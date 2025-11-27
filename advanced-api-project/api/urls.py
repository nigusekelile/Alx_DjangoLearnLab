"""
URL configuration for API application.
Defines RESTful endpoints for Book CRUD operations using HTTP methods.
"""

from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Book CRUD endpoints using RESTful conventions
    # GET /books/, POST /books/
    path('books/', views.BookListCreateView.as_view(), name='book-list-create'),
    
    # GET /books/<pk>/, PUT /books/<pk>/, PATCH /books/<pk>/, DELETE /books/<pk>/
    path('books/<int:pk>/', views.BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
    
    # Author endpoints (read-only)
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
]