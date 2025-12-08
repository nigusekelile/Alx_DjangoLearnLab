from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from .serializers import (
    UserSerializer, 
    RegisterSerializer, 
    LoginSerializer,
    ChangePasswordSerializer,
    TokenSerializer
)
from .models import CustomUser


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


class FollowUserView(APIView):
    """View to follow/unfollow a user."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, user_id):
        user_to_follow = get_object_or_404(CustomUser, id=user_id)
        current_user = request.user
        
        if current_user == user_to_follow:
            return Response(
                {"error": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if current_user.following.filter(id=user_id).exists():
            # Unfollow
            current_user.following.remove(user_to_follow)
            message = f"Unfollowed {user_to_follow.username}"
        else:
            # Follow
            current_user.following.add(user_to_follow)
            message = f"Following {user_to_follow.username}"
        
        current_user.save()
        
        return Response({
            "message": message,
            "followers_count": user_to_follow.followers_count,
            "following_count": current_user.following_count
        })