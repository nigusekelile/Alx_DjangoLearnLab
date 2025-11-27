"""
Django management command to seed test data for development and testing.
"""

from django.core.management.base import BaseCommand
from api.models import Author, Book

class Command(BaseCommand):
    help = 'Seed the database with sample authors and books'

    def handle(self, *args, **options):
        """Execute the seeding command."""
        self.stdout.write('Seeding database with sample data...')
        
        # Create authors
        authors_data = [
            {'name': 'George Orwell'},
            {'name': 'J.K. Rowling'},
            {'name': 'J.R.R. Tolkien'},
            {'name': 'Agatha Christie'},
        ]
        
        authors = []
        for author_data in authors_data:
            author, created = Author.objects.get_or_create(**author_data)
            authors.append(author)
            if created:
                self.stdout.write(f'Created author: {author.name}')
        
        # Create books
        books_data = [
            {'title': '1984', 'publication_year': 1949, 'author': authors[0]},
            {'title': 'Animal Farm', 'publication_year': 1945, 'author': authors[0]},
            {'title': "Harry Potter and the Philosopher's Stone", 'publication_year': 1997, 'author': authors[1]},
            {'title': 'The Hobbit', 'publication_year': 1937, 'author': authors[2]},
            {'title': 'The Lord of the Rings', 'publication_year': 1954, 'author': authors[2]},
            {'title': 'Murder on the Orient Express', 'publication_year': 1934, 'author': authors[3]},
        ]
        
        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults=book_data
            )
            if created:
                self.stdout.write(f'Created book: {book.title}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully seeded database with sample data!')
        )