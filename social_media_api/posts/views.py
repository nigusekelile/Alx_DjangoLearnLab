from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Post, Comment
from .serializers import (
    PostSerializer, 
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer
)
from .permissions import IsOwnerOrReadOnly


class StandardResultsSetPagination(PageNumberPagination):
    """Custom pagination class."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing posts."""
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'likes_count']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return the queryset for posts."""
        # Use Post.objects.all() as specified in requirements
        queryset = Post.objects.all().filter(is_published=True).select_related('author').prefetch_related('likes', 'comments')
        
        author = self.request.query_params.get('author')
        search_query = self.request.query_params.get('search')
        
        # Filter by author if provided
        if author:
            queryset = queryset.filter(author__username=author)
        
        # Filter by search query if provided
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        
        return queryset
    
    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action == 'list':
            return PostListSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        """Set the author to the current user when creating a post."""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like or unlike a post."""
        post = self.get_object()
        user = request.user
        
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True
        
        return Response({
            'liked': liked,
            'likes_count': post.likes_count,
            'message': 'Post liked' if liked else 'Post unliked'
        })
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get comments for a specific post."""
        post = self.get_object()
        
        # Get comments for this post
        comments = Comment.objects.all().filter(post=post).select_related('author')
        
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing comments."""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """Return the queryset for comments."""
        # Use Comment.objects.all() as specified in requirements
        queryset = Comment.objects.all().select_related('author', 'post')
        
        # Filter by post ID if provided
        post_id = self.request.query_params.get('post')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        
        # Filter by author username if provided
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author__username=author)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set the author to the current user when creating a comment."""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like or unlike a comment."""
        comment = self.get_object()
        user = request.user
        
        if comment.likes.filter(id=user.id).exists():
            comment.likes.remove(user)
            liked = False
        else:
            comment.likes.add(user)
            liked = True
        
        return Response({
            'liked': liked,
            'likes_count': comment.likes_count,
            'message': 'Comment liked' if liked else 'Comment unliked'
        })
    
    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        """Get replies for a specific comment."""
        comment = self.get_object()
        
        # Get replies for this comment
        replies = Comment.objects.all().filter(parent_comment=comment).select_related('author')
        
        page = self.paginate_queryset(replies)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = CommentSerializer(replies, many=True)
        return Response(serializer.data)