from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like
from .serializers import (
    PostSerializer, 
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer,
    FeedPostSerializer
)


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
        """Like or unlike a post (toggle)."""
        post = self.get_object()
        user = request.user
        
        # Check if already liked
        like = Like.objects.filter(user=user, post=post).first()
        
        if like:
            # Unlike
            like.delete()
            liked = False
            message = "Post unliked"
        else:
            # Like
            Like.objects.create(user=user, post=post)
            liked = True
            message = "Post liked"
            
            # Create notification (only when liking)
            NotificationManager.notify_like(user, post)
        
        return Response({
            'liked': liked,
            'likes_count': post.likes.count(),
            'message': message
        })


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
        comment = serializer.save(author=self.request.user)
        
        # Create notification for post author
        NotificationManager.notify_comment(self.request.user, comment)
    
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


class FeedView(APIView):
    """View to get the feed of posts from followed users."""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get feed posts with pagination."""
        # Get users that the current user is following
        current_user = request.user
        following_users = current_user.following.all()
        
        # Get posts from followed users that are published
        # Use the exact pattern: Post.objects.filter(author__in=following_users).order_by
        feed_posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        
        # Only include published posts
        feed_posts = feed_posts.filter(is_published=True)
        
        # Apply pagination
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(feed_posts, request)
        
        if page is not None:
            serializer = FeedPostSerializer(page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)
        
        serializer = FeedPostSerializer(feed_posts, many=True, context={'request': request})
        return Response(serializer.data)


# Add these imports at the top of the file if not already present
from notifications.models import Notification
from notifications.notify import NotificationManager


class LikePostView(APIView):
    """View to like a post."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        """Like a post."""
        # Use generics.get_object_or_404(Post, pk=pk) as specified
        post = generics.get_object_or_404(Post, pk=pk)
        user = request.user
        
        # Check if already liked
        if Like.objects.filter(user=user, post=post).exists():
            return Response(
                {"error": "You have already liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Use Like.objects.get_or_create(user=request.user, post=post) as specified
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        # Create notification using Notification.objects.create as specified
        if user != post.author:  # Don't notify if user likes their own post
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb='like',
                message=f"{user.username} liked your post: {post.title[:50]}..."
            )
        
        return Response({
            "status": "success",
            "message": "Post liked successfully",
            "like_id": like.id,
            "likes_count": post.likes_count
        }, status=status.HTTP_201_CREATED)


class UnlikePostView(APIView):
    """View to unlike a post."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        """Unlike a post."""
        # Use generics.get_object_or_404(Post, pk=pk) as specified
        post = generics.get_object_or_404(Post, pk=pk)
        user = request.user
        
        # Check if liked
        like = Like.objects.filter(user=user, post=post).first()
        if not like:
            return Response(
                {"error": "You have not liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delete like
        like_id = like.id
        like.delete()
        
        return Response({
            "status": "success",
            "message": "Post unliked successfully",
            "like_id": like_id,
            "likes_count": post.likes_count
        })


class PostLikesListView(generics.ListAPIView):
    """View to list users who liked a post."""
    serializer_class = CommentSerializer  # Temporary, we'll override the method
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request, pk):
        """Get users who liked the post."""
        post = generics.get_object_or_404(Post, pk=pk, is_published=True)
        
        # Get likes with users
        likes = Like.objects.filter(post=post).select_related('user')
        
        # Prepare response data
        likers = []
        for like in likes:
            likers.append({
                'id': like.user.id,
                'username': like.user.username,
                'profile_picture': like.user.profile_picture.url if like.user.profile_picture else None,
                'liked_at': like.created_at
            })
        
        return Response({
            'post_id': post.id,
            'post_title': post.title,
            'likes_count': post.likes_count,
            'likers': likers
        })