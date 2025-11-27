"""
URL configuration for API application.
Defines endpoints for Author and Book resources.
"""

from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('authors/', views.AuthorListCreateView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('books/', views.BookListCreateView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
]