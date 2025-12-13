from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet, 
    CommentViewSet, 
    FeedView,
    LikePostView,          # Add this
    UnlikePostView,        # Add this
    PostLikesListView      # Add this
)

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
    
    # Like endpoints
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like_post'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike_post'),
    path('posts/<int:pk>/likes/', PostLikesListView.as_view(), name='post_likes'),
]