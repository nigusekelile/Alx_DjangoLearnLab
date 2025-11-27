"""
Custom views for the API application.
Implements generic views for CRUD operations on Book model with custom behavior
and permission controls.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

class BookListView(generics.ListAPIView):
    """
    List view for retrieving all books with filtering and search capabilities.
    
    Features:
    - Lists all book instances
    - Supports filtering by publication_year and author
    - Provides search functionality on title field
    - Allows ordering by multiple fields
    - Open to all users (including unauthenticated)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Read-only access for all
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['publication_year', 'author']
    search_fields = ['title']
    ordering_fields = ['title', 'publication_year', 'created_at']
    ordering = ['title']  # Default ordering

class BookDetailView(generics.RetrieveAPIView):
    """
    Detail view for retrieving a single book by ID.
    
    Features:
    - Retrieves specific book instance by primary key
    - Includes nested author information
    - Open to all users (including unauthenticated)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'

class BookCreateView(generics.CreateAPIView):
    """
    Create view for adding new books with custom validation.
    
    Features:
    - Handles book creation with data validation
    - Applies custom publication_year validation
    - Restricted to authenticated users only
    - Custom success response with created book data
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom method called when creating a new book instance.
        
        Args:
            serializer: Validated book serializer instance
        """
        serializer.save()

    def create(self, request, *args, **kwargs):
        """
        Override create method to customize response format.
        
        Returns:
            Response: Custom response with success message and book data
        """
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
    """
    Update view for modifying existing books with partial updates support.
    
    Features:
    - Handles full (PUT) and partial (PATCH) updates
    - Applies validation on updated data
    - Restricted to authenticated users only
    - Custom response format
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        """
        Override update method to customize response format.
        
        Returns:
            Response: Custom response with success message and updated book data
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(
            {
                'message': 'Book updated successfully',
                'book': serializer.data
            }
        )

    def perform_update(self, serializer):
        """Save the updated book instance."""
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        """Handle PATCH requests for partial updates."""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

class BookDeleteView(generics.DestroyAPIView):
    """
    Delete view for removing books with custom response.
    
    Features:
    - Handles book deletion
    - Restricted to authenticated users only
    - Custom success response without returning deleted data
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        """
        Override destroy method to customize response format.
        
        Returns:
            Response: Custom success message without returning deleted data
        """
        instance = self.get_object()
        book_title = instance.title
        self.perform_destroy(instance)
        
        return Response(
            {
                'message': f'Book "{book_title}" deleted successfully'
            },
            status=status.HTTP_200_OK
        )

    def perform_destroy(self, instance):
        """Delete the book instance."""
        instance.delete()

# Author views for completeness
class AuthorListView(generics.ListAPIView):
    """List view for authors with books count"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

class AuthorDetailView(generics.RetrieveAPIView):
    """Detail view for authors with nested books"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]

from .permissions import IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly

# Update BookCreateView, BookUpdateView, BookDeleteView permissions
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Or use [IsAuthenticatedOrReadOnly]

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Or use [IsAuthenticatedOrReadOnly]

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Or use [IsAuthenticatedOrReadOnly]