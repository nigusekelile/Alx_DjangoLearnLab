# relationship_app/management/commands/populate_books.py
from django.core.management.base import BaseCommand
from relationship_app.models import Author, Book, Library, Librarian

class Command(BaseCommand):
    help = 'Populate database with sample books and authors'

    def handle(self, *args, **options):
        # Clear existing data
        Book.objects.all().delete()
        Author.objects.all().delete()
        Library.objects.all().delete()
        Librarian.objects.all().delete()

        self.stdout.write("📚 Creating sample books and authors...")
        
        # Create authors
        authors = [
            Author.objects.create(name="J.K. Rowling"),
            Author.objects.create(name="George Orwell"),
            Author.objects.create(name="Agatha Christie"),
            Author.objects.create(name="J.R.R. Tolkien"),
            Author.objects.create(name="Stephen King"),
        ]
        
        # Create books
        books = [
            Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=authors[0], publication_year=1997),
            Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=authors[0], publication_year=1998),
            Book.objects.create(title="1984", author=authors[1], publication_year=1949),
            Book.objects.create(title="Animal Farm", author=authors[1], publication_year=1945),
            Book.objects.create(title="Murder on the Orient Express", author=authors[2], publication_year=1934),
            Book.objects.create(title="The Hobbit", author=authors[3], publication_year=1937),
            Book.objects.create(title="The Lord of the Rings", author=authors[3], publication_year=1954),
            Book.objects.create(title="The Shining", author=authors[4], publication_year=1977),
        ]
        
        # Create libraries and assign books
        library1 = Library.objects.create(name="City Central Library")
        library2 = Library.objects.create(name="University Library")
        
        library1.books.add(books[0], books[1], books[2], books[4])
        library2.books.add(books[3], books[5], books[6], books[7])
        
        # Create librarians
        Librarian.objects.create(name="Alice Johnson", library=library1)
        Librarian.objects.create(name="Bob Smith", library=library2)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Successfully created sample data!\n'
                f'   - Authors: {len(authors)}\n'
                f'   - Books: {len(books)}\n'
                f'   - Libraries: 2\n'
                f'   - Librarians: 2'
            )
        )
        
        # Display book IDs for testing
        self.stdout.write("\n📖 Book IDs for testing:")
        for book in books:
            self.stdout.write(f'   - {book.id}: {book.title}')
