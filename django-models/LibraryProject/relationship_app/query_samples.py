# relationship_app/query_samples.py
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def query_all_books_by_author(author_name):
    """
    Query all books by a specific author
    """
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()  # Using related_name 'books'
        print(f"All books by {author_name}:")
        for book in books:
            print(f"- {book.title}")
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return []

def list_all_books_in_library(library_name):
    """
    List all books in a specific library
    """
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()  # Using ManyToMany relationship
        print(f"All books in {library_name} library:")
        for book in books:
            print(f"- {book.title} (by {book.author.name})")
        return books
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return []

def retrieve_librarian_for_library(library_name):
    """
    Retrieve the librarian for a specific library
    """
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian  # Using OneToOne relationship
        print(f"Librarian for {library_name}: {librarian.name}")
        return librarian
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None
    except Librarian.DoesNotExist:
        print(f"No librarian found for {library_name}.")
        return None

def create_sample_data():
    """
    Create sample data to test the queries
    """
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    
    # Create books
    book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1)
    book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1)
    book3 = Book.objects.create(title="1984", author=author2)
    book4 = Book.objects.create(title="Animal Farm", author=author2)
    
    # Create library
    library = Library.objects.create(name="City Central Library")
    library.books.add(book1, book2, book3)
    
    # Create librarian
    librarian = Librarian.objects.create(name="Alice Johnson", library=library)
    
    return author1, author2, library, librarian

if __name__ == "__main__":
    print("Creating sample data...")
    create_sample_data()
    
    print("\n" + "="*50)
    print("DEMONSTRATING RELATIONSHIP QUERIES")
    print("="*50)
    
    # Query 1: All books by a specific author
    print("\n1. Query all books by a specific author:")
    query_all_books_by_author("J.K. Rowling")
    
    # Query 2: List all books in a library
    print("\n2. List all books in a library:")
    list_all_books_in_library("City Central Library")
    
    # Query 3: Retrieve librarian for a library
    print("\n3. Retrieve librarian for a library:")
    retrieve_librarian_for_library("City Central Library")
