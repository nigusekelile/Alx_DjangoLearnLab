"""
Custom views for the API application.
Implements generic views for CRUD operations on Book model with RESTful endpoints.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

class BookListCreateView(generics.ListCreateAPIView):
    """
    Combined list and create view for books.
    
    Handles:
    - GET: Returns list of all books (public access)
    - POST: Creates a new book (authenticated users only)
    
    Features:
    - Filtering, searching, and ordering for GET requests
    - Custom validation and response for POST requests
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['publication_year', 'author']
    search_fields = ['title']
    ordering_fields = ['title', 'publication_year', 'created_at']
    ordering = ['title']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        - GET: AllowAny
        - POST: IsAuthenticated
        """
        if self.request.method == 'GET':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

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

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Combined retrieve, update, and destroy view for individual books.
    
    Handles:
    - GET: Retrieve single book (public access)
    - PUT: Full update of book (authenticated users only)
    - PATCH: Partial update of book (authenticated users only)
    - DELETE: Remove book (authenticated users only)
    
    Features:
    - Custom responses for update and delete operations
    - Proper permission handling per HTTP method
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        - GET: AllowAny
        - PUT, PATCH, DELETE: IsAuthenticated
        """
        if self.request.method == 'GET':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

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

# Keep the existing Author views
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