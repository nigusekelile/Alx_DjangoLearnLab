"""
Basic views for testing serializers.
Provides simple list and detail views for Author and Book models.
"""

from rest_framework import generics
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

class AuthorListCreateView(generics.ListCreateAPIView):
    """View for listing and creating authors"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorDetailView(generics.RetrieveAPIView):
    """View for retrieving author details"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookListCreateView(generics.ListCreateAPIView):
    """View for listing and creating books"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailView(generics.RetrieveAPIView):
    """View for retrieving book details"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer