# relationship_app/management/commands/populate_sample_data.py
from django.core.management.base import BaseCommand
from relationship_app.models import Author, Book, Library, Librarian

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        # Clear existing data
        Book.objects.all().delete()
        Author.objects.all().delete()
        Library.objects.all().delete()
        Librarian.objects.all().delete()

        # Create authors
        author1 = Author.objects.create(name="J.K. Rowling")
        author2 = Author.objects.create(name="George Orwell")
        author3 = Author.objects.create(name="Agatha Christie")
        
        # Create books
        book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1, publication_year=1997)
        book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1, publication_year=1998)
        book3 = Book.objects.create(title="1984", author=author2, publication_year=1949)
        book4 = Book.objects.create(title="Animal Farm", author=author2, publication_year=1945)
        book5 = Book.objects.create(title="Murder on the Orient Express", author=author3, publication_year=1934)
        
        # Create libraries
        library1 = Library.objects.create(name="City Central Library")
        library2 = Library.objects.create(name="University Library")
        
        # Add books to libraries
        library1.books.add(book1, book2, book3)
        library2.books.add(book3, book4, book5)
        
        # Create librarians
        Librarian.objects.create(name="Alice Johnson", library=library1)
        Librarian.objects.create(name="Bob Smith", library=library2)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated sample data!')
        )
