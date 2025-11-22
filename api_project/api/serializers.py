# api/serializers.py

from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_title(self, value):
        """
        Custom validation for title field
        """
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Title must be at least 2 characters long.")
        return value
    
    def validate_author(self, value):
        """
        Custom validation for author field
        """
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Author name must be at least 2 characters long.")
        return value