"""
Custom filter classes for advanced filtering capabilities.
Provides enhanced filtering options for Book model with range lookups and exact matches.
"""

import django_filters
from django_filters import rest_framework as filters
from .models import Book, Author

class BookFilter(django_filters.FilterSet):
    """
    Custom filter set for Book model with advanced filtering options.
    
    Features:
    - Exact matching on publication_year and author
    - Range filtering on publication_year
    - Case-insensitive contains filtering on title
    - Multiple field lookups for flexible querying
    """
    
    # Exact match filtering
    publication_year = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='exact',
        help_text="Exact year of publication"
    )
    
    # Range filtering for publication year
    publication_year_min = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='gte',
        help_text="Minimum publication year"
    )
    publication_year_max = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='lte',
        help_text="Maximum publication year"
    )
    
    # Multiple field lookups for title
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        help_text="Title contains (case-insensitive)"
    )
    title_exact = django_filters.CharFilter(
        field_name='title',
        lookup_expr='exact',
        help_text="Exact title match"
    )
    
    # Author filtering
    author = django_filters.NumberFilter(
        field_name='author__id',
        help_text="Author ID"
    )
    author_name = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains',
        help_text="Author name contains (case-insensitive)"
    )
    
    # Combined search field
    search = django_filters.CharFilter(
        method='filter_search',
        help_text="Search in title and author name"
    )
    
    class Meta:
        model = Book
        fields = {
            'publication_year': ['exact', 'gte', 'lte'],
            'title': ['exact', 'icontains'],
            'author__name': ['exact', 'icontains'],
        }
    
    def filter_search(self, queryset, name, value):
        """
        Custom search method that searches across multiple fields.
        
        Args:
            queryset: The original queryset
            name: Field name (unused)
            value: Search term
            
        Returns:
            QuerySet: Filtered queryset containing search term in title or author name
        """
        if value:
            return queryset.filter(
                models.Q(title__icontains=value) |
                models.Q(author__name__icontains=value)
            )
        return queryset

class AuthorFilter(django_filters.FilterSet):
    """
    Filter set for Author model with book count filtering.
    """
    
    book_count_min = django_filters.NumberFilter(
        method='filter_book_count_min',
        help_text="Minimum number of books by author"
    )
    book_count_max = django_filters.NumberFilter(
        method='filter_book_count_max',
        help_text="Maximum number of books by author"
    )
    
    class Meta:
        model = Author
        fields = {
            'name': ['exact', 'icontains'],
        }
    
    def filter_book_count_min(self, queryset, name, value):
        """Filter authors with minimum book count"""
        if value:
            return queryset.annotate(book_count=models.Count('books')).filter(book_count__gte=value)
        return queryset
    
    def filter_book_count_max(self, queryset, name, value):
        """Filter authors with maximum book count"""
        if value:
            return queryset.annotate(book_count=models.Count('books')).filter(book_count__lte=value)
        return queryset