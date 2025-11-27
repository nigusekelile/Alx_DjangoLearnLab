"""
Enhanced views with comprehensive filtering, searching, and ordering capabilities.
Implements advanced query features for Book and Author models.
"""
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import models
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from .filters import BookFilter, AuthorFilter

class BookListView(generics.ListAPIView):
    """
    Enhanced list view for books with comprehensive filtering, searching, and ordering.
    
    URL: GET /api/books/
    
    Filtering Features:
    - Exact filtering: publication_year, author
    - Range filtering: publication_year_min, publication_year_max
    - Text filtering: title, author_name
    - Combined search: search (across title and author name)
    
    Search Features:
    - Search across: title, author__name
    
    Ordering Features:
    - Order by: title, publication_year, created_at, updated_at, author__name
    - Default ordering: title ascending
    
    Example Queries:
    - /api/books/?publication_year=2020
    - /api/books/?publication_year_min=2010&publication_year_max=2020
    - /api/books/?title=harry
    - /api/books/?author_name=rowling
    - /api/books/?search=magic
    - /api/books/?ordering=-publication_year,title
    """
    
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    # Filter backends configuration
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Django Filter configuration
    filterset_class = BookFilter
    
    # Search configuration
    search_fields = [
        'title',
        'author__name',
        'publication_year',
    ]
    
    # Ordering configuration
    ordering_fields = [
        'title',
        'publication_year', 
        'created_at',
        'updated_at',
        'author__name',
    ]
    ordering = ['title']  # Default ordering
    
    def get_queryset(self):
        """
        Enhance base queryset with annotations for advanced filtering.
        """
        queryset = super().get_queryset()
        
        # Add annotation for decade (example of computed field)
        queryset = queryset.annotate(
            decade=(models.F('publication_year') / 10) * 10
        )
        
        return queryset

class BookDetailView(generics.RetrieveAPIView):
    """Detail view for individual books"""
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'

class BookCreateView(generics.CreateAPIView):
    """Create view for new books"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Custom create response"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        return Response(
            {
                'message': 'Book created successfully',
                'book': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class BookUpdateView(generics.UpdateAPIView):
    """Update view for existing books"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        """Custom update response"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {
                'message': 'Book updated successfully',
                'book': serializer.data
            }
        )

class BookDeleteView(generics.DestroyAPIView):
    """Delete view for books"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        """Custom delete response"""
        instance = self.get_object()
        book_title = instance.title
        self.perform_destroy(instance)
        
        return Response(
            {
                'message': f'Book "{book_title}" deleted successfully'
            },
            status=status.HTTP_200_OK
        )

class AuthorListView(generics.ListAPIView):
    """
    Enhanced list view for authors with filtering and ordering.
    
    URL: GET /api/authors/
    
    Filtering Features:
    - Name filtering: exact and contains
    - Book count filtering: book_count_min, book_count_max
    
    Ordering Features:
    - Order by: name, created_at, book_count
    - Default ordering: name ascending
    """
    
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AuthorFilter
    search_fields = ['name']
    ordering_fields = ['name', 'created_at', 'book_count']
    ordering = ['name']
    
    def get_queryset(self):
        """
        Enhance queryset with book count annotation.
        """
        queryset = super().get_queryset()
        return queryset.annotate(book_count=models.Count('books'))

class AuthorDetailView(generics.RetrieveAPIView):
    """Detail view for authors"""
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]