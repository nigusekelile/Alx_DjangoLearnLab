from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    TokenRetrieveView,
    UserProfileView,
    ChangePasswordView,
    FollowUserView,
    FollowManagementView,  # Add this
    UserFollowersView,     # Add this
    UserFollowingView,     # Add this
    UserSearchView         # Add this
)

urlpatterns = [
    # Authentication endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/', TokenRetrieveView.as_view(), name='token-retrieve'),
    
    # User profile endpoints
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    
    # Follow/unfollow endpoints (keep the old one for compatibility)
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow_user'),
    
    # New follow management endpoints
    path('users/<int:user_id>/follow/', FollowManagementView.as_view(), name='follow_management'),
    path('users/<int:user_id>/followers/', UserFollowersView.as_view(), name='user_followers'),
    path('users/<int:user_id>/following/', UserFollowingView.as_view(), name='user_following'),
    
    # User search endpoint
    path('users/search/', UserSearchView.as_view(), name='user_search'),
]