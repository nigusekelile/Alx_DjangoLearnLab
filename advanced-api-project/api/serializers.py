"""
Custom serializers for the API application.
Handles serialization of Author and Book models with nested relationships
and custom validation logic.
"""

from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model with custom validation.
    
    Handles:
    - Serialization of all Book model fields
    - Custom validation for publication_year to ensure it's not in the future
    - Representation of related author information
    
    Validation:
    - publication_year: Ensures the year is not greater than current year
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If publication year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value
    
    def to_representation(self, instance):
        """
        Custom representation to include author name in book serialization.
        
        Args:
            instance: Book model instance
            
        Returns:
            dict: Serialized book data with author name
        """
        representation = super().to_representation(instance)
        representation['author_name'] = instance.author.name
        return representation

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model with nested Book serialization.
    
    Handles:
    - Serialization of author fields
    - Dynamic nested serialization of related books using BookSerializer
    - Read-only books field for GET requests
    
    Nested Relationships:
    - books: Uses BookSerializer to serialize all books by this author
    - The books field is read-only and only included in GET responses
    """
    
    # Nested serializer for related books
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'books']
    
    def to_representation(self, instance):
        """
        Custom representation to handle nested book data.
        
        Args:
            instance: Author model instance
            
        Returns:
            dict: Serialized author data with nested books
        """
        representation = super().to_representation(instance)
        
        # Include book count for additional context
        representation['book_count'] = instance.books.count()
        
        return representation