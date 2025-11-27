"""
Data models for the API application.
Defines Author and Book models with one-to-many relationship.
"""

from django.db import models

class Author(models.Model):
    """
    Author model representing a book author.
    
    Fields:
    - name: CharField - The author's full name
    - created_at: DateTimeField - Automatic timestamp when author is created
    - updated_at: DateTimeField - Automatic timestamp when author is updated
    """
    name = models.CharField(
        max_length=200,
        help_text="Full name of the author"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
    
    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Book model representing a published book.
    
    Fields:
    - title: CharField - The book's title
    - publication_year: IntegerField - Year the book was published
    - author: ForeignKey - Reference to the Author model (one-to-many relationship)
    - created_at: DateTimeField - Automatic timestamp when book is created
    - updated_at: DateTimeField - Automatic timestamp when book is updated
    
    Relationship:
    - Each Author can have multiple Books (one-to-many)
    - Book.author references Author model with CASCADE delete
    """
    title = models.CharField(
        max_length=300,
        help_text="Title of the book"
    )
    publication_year = models.IntegerField(
        help_text="Year the book was published"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        help_text="Author of the book"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['title']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        unique_together = ['title', 'author']
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"