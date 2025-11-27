"""
Enhanced serializers with filtering context support.
"""

from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Enhanced Book serializer with filtering-friendly fields.
    """
    author_name = serializers.CharField(source='author.name', read_only=True)
    decade = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'publication_year', 'author', 'author_name',
            'decade', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'author_name', 'decade']
    
    def get_decade(self, obj):
        """Calculate the decade for the publication year."""
        if obj.publication_year:
            return (obj.publication_year // 10) * 10
        return None
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        if value < 1000:
            raise serializers.ValidationError(
                "Publication year must be a valid year."
            )
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Enhanced Author serializer with book count and nested books.
    """
    books = BookSerializer(many=True, read_only=True)
    book_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books', 'book_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'books', 'book_count']