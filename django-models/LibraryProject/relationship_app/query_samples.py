# relationship_app/query_samples.py
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def query_all_books_by_author(author_name):
    """
    Query all books by a specific author using objects.filter()
    """
    try:
        author = Author.objects.get(name=author_name)
        # Using objects.filter(author=author) as requested
        books = Book.objects.filter(author=author)
        print(f"All books by {author_name} (using objects.filter):")
        for book in books:
            print(f"- {book.title}")
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return []

def query_all_books_by_author_reverse(author_name):
    """
    Alternative approach using reverse relationship
    """
    try:
        author = Author.objects.get(name=author_name)
        # Using reverse relationship (author.books.all())
        books = author.books.all()
        print(f"All books by {author_name} (using reverse relationship):")
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

def demonstrate_additional_queries():
    """
    Demonstrate additional relationship queries
    """
    print("\n" + "="*50)
    print("ADDITIONAL RELATIONSHIP QUERIES")
    print("="*50)
    
    # Query books by author using filter with field lookup
    print("\n4. Books by J.K. Rowling (using __name lookup):")
    books = Book.objects.filter(author__name="J.K. Rowling")
    for book in books:
        print(f"- {book.title}")
    
    # Query libraries that contain books by a specific author
    print("\n5. Libraries with books by George Orwell:")
    libraries = Library.objects.filter(books__author__name="George Orwell").distinct()
    for library in libraries:
        print(f"- {library.name}")
    
    # Query using exclude
    print("\n6. Books NOT by J.K. Rowling:")
    books = Book.objects.exclude(author__name="J.K. Rowling")
    for book in books:
        print(f"- {book.title} by {book.author.name}")

def create_sample_data():
    """
    Create sample data to test the queries
    """
    # Clear existing sample data to avoid duplicates
    Book.objects.filter(author__name__in=["J.K. Rowling", "George Orwell"]).delete()
    Author.objects.filter(name__in=["J.K. Rowling", "George Orwell"]).delete()
    Library.objects.filter(name="City Central Library").delete()
    
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
    
    # Query 1: All books by a specific author using objects.filter()
    print("\n1. Query all books by a specific author (using objects.filter):")
    query_all_books_by_author("J.K. Rowling")
    
    # Query 1b: Alternative approach using reverse relationship
    print("\n1b. Query all books by a specific author (using reverse relationship):")
    query_all_books_by_author_reverse("J.K. Rowling")
    
    # Query 2: List all books in a library
    print("\n2. List all books in a library:")
    list_all_books_in_library("City Central Library")
    
    # Query 3: Retrieve librarian for a library
    print("\n3. Retrieve librarian for a library:")
    retrieve_librarian_for_library("City Central Library")
    
    # Demonstrate additional queries
    demonstrate_additional_queries()
    
    # Show the SQL queries being generated
    print("\n" + "="*50)
    print("SQL QUERIES GENERATED")
    print("="*50)
    
    from django.db import connection
    
    # Reset connection for SQL logging
    connection.queries_log.clear()
    
    # Execute a sample query and show SQL
    books = Book.objects.filter(author__name="J.K. Rowling")
    list(books)  # Force query execution
    
    if connection.queries:
        print(f"SQL for Book.objects.filter(author__name='J.K. Rowling'):")
        print(connection.queries[-1]['sql'])
