from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    TokenRetrieveView,
    UserProfileView,
    ChangePasswordView,
    FollowUserView,
    UnfollowUserView,  # Add this import
    UserFollowersView,
    UserFollowingView,
    UserSearchView
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
    
    # Follow/unfollow endpoints
    # The toggle endpoint that can both follow and unfollow
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow_user'),
    
    # Specific unfollow endpoint as requested in the task
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow_user'),
    
    # User followers/following endpoints
    path('users/<int:user_id>/followers/', UserFollowersView.as_view(), name='user_followers'),
    path('users/<int:user_id>/following/', UserFollowingView.as_view(), name='user_following'),
    
    # User search endpoint
    path('users/search/', UserSearchView.as_view(), name='user_search'),
]