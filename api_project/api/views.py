# api/views.py

from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Book
from .serializers import BookSerializer, UserRegistrationSerializer
from .permissions import IsAdminOrReadOnly

# User Registration View
class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    Creates a new user and returns an authentication token.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create token for the new user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token.key,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)

# Public Book List View
class BookList(generics.ListAPIView):
    """
    API endpoint that allows books to be viewed (read-only).
    Public access for listing books.
    """
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

# Book ViewSet with authentication
class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing book instances.
    Provides full CRUD operations: list, create, retrieve, update, destroy
    """
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
    
    # Use custom permission: admins can do anything, authenticated users can only view
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    
    def get_permissions(self):
        """
        Optionally override to use different permissions for different actions
        """
        if self.action == 'list' or self.action == 'retrieve':
            # Allow any authenticated user to view
            permission_classes = [permissions.IsAuthenticated]
        else:
            # Only allow admin users to create, update, delete
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        return [permission() for permission in permission_classes]