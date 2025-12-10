from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from .models import CustomUser, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['website', 'location', 'birth_date']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='user_profile', read_only=True)
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'bio', 'profile_picture', 'followers_count', 'following_count',
            'date_joined', 'is_verified', 'profile'
        ]
        read_only_fields = ['date_joined', 'is_verified']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Check if username already exists
        if CustomUser.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists."})
        
        # Check if email already exists
        if attrs.get('email') and CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists."})
            
        return attrs
    
    def create(self, validated_data):
        # Remove password2 from validated data
        validated_data.pop('password2')
        
        # Use get_user_model().objects.create_user() as specified in requirements
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        # Create token for the user
        Token.objects.create(user=user)
        
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            # Use authenticate to validate credentials
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                data['user'] = user
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")
        
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True, 
        validators=[validate_password]
    )
    new_password2 = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs


class TokenSerializer(serializers.ModelSerializer):
    """Serializer for Token model"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Token
        fields = ['key', 'user', 'created']
        read_only_fields = ['key', 'user', 'created']

# Add these serializers to the end of the file

class UserFollowSerializer(serializers.ModelSerializer):
    """Lightweight serializer for follow operations."""
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    is_following = serializers.SerializerMethodField()
    
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'profile_picture', 'followers_count', 'following_count', 'is_following']
    
    def get_is_following(self, obj):
        """Check if the current user is following this user."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)
        return False


class FollowActionSerializer(serializers.Serializer):
    """Serializer for follow/unfollow actions."""
    action = serializers.ChoiceField(choices=['follow', 'unfollow'])
    
    def validate(self, data):
        user_to_follow = self.context.get('user_to_follow')
        current_user = self.context.get('current_user')
        
        if user_to_follow == current_user:
            raise serializers.ValidationError("You cannot follow yourself.")
        
        if data['action'] == 'follow' and current_user.is_following(user_to_follow):
            raise serializers.ValidationError("You are already following this user.")
        
        if data['action'] == 'unfollow' and not current_user.is_following(user_to_follow):
            raise serializers.ValidationError("You are not following this user.")
        
        return data


class UserFollowersSerializer(serializers.ModelSerializer):
    """Serializer for listing a user's followers."""
    followers = UserFollowSerializer(many=True, read_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'followers_count', 'followers']


class UserFollowingSerializer(serializers.ModelSerializer):
    """Serializer for listing who a user is following."""
    following = UserFollowSerializer(many=True, read_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'following_count', 'following']