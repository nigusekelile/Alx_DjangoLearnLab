from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    TokenRetrieveView,
    UserProfileView,
    ChangePasswordView,
    FollowUserView
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
    
    # Follow/unfollow endpoint
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow_user'),
]