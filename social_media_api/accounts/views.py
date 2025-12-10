from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.db import models
from .serializers import (
    UserSerializer, 
    RegisterSerializer, 
    LoginSerializer,
    ChangePasswordSerializer,
    TokenSerializer,
    UserFollowSerializer, 
    FollowActionSerializer,
    UserFollowersSerializer,
    UserFollowingSerializer
)
from .models import CustomUser, UserProfile


class RegisterView(generics.CreateAPIView):
    """View for user registration."""
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Get the token that was created in the serializer
        token = Token.objects.get(user=user)
        
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key,
            "message": "User created successfully"
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """View for user login."""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            
            # Get or create token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                "user": UserSerializer(user).data,
                "token": token.key,
                "message": "Login successful"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """View for user logout."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Delete the token
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            token_message = "Token deleted successfully"
        except Token.DoesNotExist:
            token_message = "No token found for user"
        
        logout(request)
        return Response({
            "message": "Successfully logged out",
            "token_deleted": token_message
        }, status=status.HTTP_200_OK)


class TokenRetrieveView(APIView):
    """View to retrieve current user's token."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            token = Token.objects.get(user=request.user)
            serializer = TokenSerializer(token)
            return Response(serializer.data)
        except Token.DoesNotExist:
            # Create token if it doesn't exist
            token = Token.objects.create(user=request.user)
            serializer = TokenSerializer(token)
            return Response(serializer.data)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """View to retrieve and update user profile."""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    """View for changing user password."""
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Set new password
            user.set_password(serializer.data.get("new_password"))
            user.save()
            
            # Update token - delete old and create new
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            
            return Response({
                "message": "Password updated successfully",
                "token": token.key
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowUserView(generics.GenericAPIView):
    """View for following/unfollowing users using generics.GenericAPIView."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, user_id):
        """Follow or unfollow a user."""
        # Use CustomUser.objects.all() as specified
        user_to_follow = get_object_or_404(CustomUser.objects.all(), id=user_id)
        current_user = request.user
        
        if user_to_follow == current_user:
            return Response(
                {"error": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already following
        is_following = current_user.is_following(user_to_follow)
        
        if is_following:
            # Unfollow
            current_user.unfollow(user_to_follow)
            action = 'unfollowed'
        else:
            # Follow
            current_user.follow(user_to_follow)
            action = 'followed'
        
        return Response({
            "action": action,
            "user_id": user_id,
            "username": user_to_follow.username,
            "following_count": current_user.following_count,
            "followers_count": user_to_follow.followers_count,
            "is_following": not is_following
        })


class UnfollowUserView(generics.GenericAPIView):
    """View specifically for unfollowing users."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, user_id):
        """Unfollow a user."""
        # Use CustomUser.objects.all() as specified
        user_to_unfollow = get_object_or_404(CustomUser.objects.all(), id=user_id)
        current_user = request.user
        
        if user_to_unfollow == current_user:
            return Response(
                {"error": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not current_user.is_following(user_to_unfollow):
            return Response(
                {"error": "You are not following this user."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Unfollow
        current_user.unfollow(user_to_unfollow)
        
        return Response({
            "action": "unfollowed",
            "user_id": user_id,
            "username": user_to_unfollow.username,
            "following_count": current_user.following_count,
            "followers_count": user_to_unfollow.followers_count,
            "is_following": False
        })


class UserFollowersView(generics.GenericAPIView):
    """View to get a user's followers."""
    serializer_class = UserFollowersSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request, user_id):
        """Get followers of a specific user."""
        # Use CustomUser.objects.all() as specified
        user = get_object_or_404(CustomUser.objects.all(), id=user_id)
        
        # Get followers with pagination
        followers = user.followers.all()
        page = self.paginate_queryset(followers)
        
        if page is not None:
            serializer = UserFollowSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = UserFollowSerializer(followers, many=True, context={'request': request})
        return Response({
            'user_id': user.id,
            'username': user.username,
            'followers_count': user.followers_count,
            'followers': serializer.data
        })


class UserFollowingView(generics.GenericAPIView):
    """View to get who a user is following."""
    serializer_class = UserFollowingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request, user_id):
        """Get users that a specific user is following."""
        # Use CustomUser.objects.all() as specified
        user = get_object_or_404(CustomUser.objects.all(), id=user_id)
        
        # Get following with pagination
        following = user.following.all()
        page = self.paginate_queryset(following)
        
        if page is not None:
            serializer = UserFollowSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = UserFollowSerializer(following, many=True, context={'request': request})
        return Response({
            'user_id': user.id,
            'username': user.username,
            'following_count': user.following_count,
            'following': serializer.data
        })


class UserSearchView(generics.GenericAPIView):
    """View to search for users."""
    serializer_class = UserFollowSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Search for users."""
        query = request.query_params.get('q', '')
        
        if not query:
            return Response(
                {"error": "Search query parameter 'q' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Use CustomUser.objects.all() as specified
        queryset = CustomUser.objects.all().filter(
            models.Q(username__icontains=query) |
            models.Q(first_name__icontains=query) |
            models.Q(last_name__icontains=query)
        ).exclude(id=request.user.id)
        
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)