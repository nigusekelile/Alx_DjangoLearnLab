from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment
from accounts.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments."""
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        source='author',
        write_only=True
    )
    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(),
        source='post',
        write_only=True
    )
    likes_count = serializers.IntegerField(read_only=True)
    replies_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'post_id', 'author', 'author_id', 
            'content', 'parent_comment', 'created_at', 'updated_at',
            'likes_count', 'replies_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'author', 'post']
    
    def create(self, validated_data):
        # Ensure the author is the current user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    """Serializer for posts."""
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        source='author',
        write_only=True
    )
    comments_count = serializers.IntegerField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'author', 'author_id', 'title', 'content', 'image',
            'created_at', 'updated_at', 'is_published', 'likes_count',
            'comments_count', 'comments'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'author']
    
    def create(self, validated_data):
        # Ensure the author is the current user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostListSerializer(serializers.ModelSerializer):
    """Serializer for listing posts (lightweight version)."""
    author = UserSerializer(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    excerpt = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'author', 'title', 'excerpt', 'image', 
            'created_at', 'likes_count', 'comments_count'
        ]
    
    def get_excerpt(self, obj):
        """Return first 150 characters of content as excerpt."""
        return obj.content[:150] + '...' if len(obj.content) > 150 else obj.content


class PostDetailSerializer(PostSerializer):
    """Serializer for detailed post view."""
    pass  # Same as PostSerializer, can be extended if needed

# Add to posts/serializers.py

class FeedPostSerializer(PostSerializer):
    """Serializer for feed posts with additional follow context."""
    class Meta(PostSerializer.Meta):
        fields = [
            'id', 'author', 'title', 'content', 'image',
            'created_at', 'likes_count', 'comments_count'
        ]