"""
Custom views for the API application.
Implements all required generic views for complete Book CRUD operations.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

class BookListView(generics.ListAPIView):
    """
    List view for retrieving all books.
    
    URL: GET /api/books/
    Permissions: AllowAny (public access)
    Features: Filtering, searching, ordering
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['publication_year', 'author']
    search_fields = ['title']
    ordering_fields = ['title', 'publication_year', 'created_at']
    ordering = ['title']

class BookDetailView(generics.RetrieveAPIView):
    """
    Detail view for retrieving a single book by ID.
    
    URL: GET /api/books/<pk>/
    Permissions: AllowAny (public access)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'

class BookCreateView(generics.CreateAPIView):
    """
    Create view for adding new books.
    
    URL: POST /api/books/create/
    Permissions: IsAuthenticated
    Features: Custom validation and response format
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Override create method to customize response format.
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
    Update view for modifying existing books.
    
    URL: PUT/PATCH /api/books/<pk>/update/
    Permissions: IsAuthenticated
    Features: Supports both full and partial updates
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        """
        Override update method to customize response format.
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

    def partial_update(self, request, *args, **kwargs):
        """Handle PATCH requests for partial updates."""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

class BookDeleteView(generics.DestroyAPIView):
    """
    Delete view for removing books.
    
    URL: DELETE /api/books/<pk>/delete/
    Permissions: IsAuthenticated
    Features: Custom success response
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        """
        Override destroy method to customize response format.
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

# Author views (read-only)
class AuthorListView(generics.ListAPIView):
    """List view for authors"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

class AuthorDetailView(generics.RetrieveAPIView):
    """Detail view for authors"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]