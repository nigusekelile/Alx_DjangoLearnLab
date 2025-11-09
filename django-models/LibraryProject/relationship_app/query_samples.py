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
    Retrieve the librarian for a specific library using Librarian.objects.get(library=...)
    """
    try:
        library = Library.objects.get(name=library_name)
        # Using Librarian.objects.get(library=library) as requested
        librarian = Librarian.objects.get(library=library)
        print(f"Librarian for {library_name}: {librarian.name}")
        return librarian
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None
    except Librarian.DoesNotExist:
        print(f"No librarian found for {library_name}.")
        return None

def retrieve_librarian_alternative(library_name):
    """
    Alternative approach using reverse relationship (for comparison)
    """
    try:
        library = Library.objects.get(name=library_name)
        # Using reverse OneToOne relationship
        librarian = library.librarian
        print(f"Librarian for {library_name} (using reverse relationship): {librarian.name}")
        return librarian
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None
    except Librarian.DoesNotExist:
        print(f"No librarian found for {library_name}.")
        return None

def demonstrate_all_relationship_queries():
    """
    Demonstrate all three relationship types with different query approaches
    """
    print("\n" + "="*60)
    print("COMPREHENSIVE RELATIONSHIP QUERY DEMONSTRATION")
    print("="*60)
    
    # 1. ForeignKey relationships
    print("\n1. FOREIGNKEY RELATIONSHIPS:")
    print("-" * 30)
    
    # Approach 1: Using objects.filter()
    print("a) Using Book.objects.filter(author=author):")
    try:
        author = Author.objects.get(name="J.K. Rowling")
        books = Book.objects.filter(author=author)
        for book in books:
            print(f"  - {book.title}")
    except Author.DoesNotExist:
        print("  Author not found")
    
    # Approach 2: Using __ lookup
    print("\nb) Using Book.objects.filter(author__name='J.K. Rowling'):")
    books = Book.objects.filter(author__name="J.K. Rowling")
    for book in books:
        print(f"  - {book.title}")
    
    # 2. ManyToMany relationships
    print("\n2. MANYTOMANY RELATIONSHIPS:")
    print("-" * 30)
    
    # Approach 1: Using library.books.all()
    print("a) Using library.books.all():")
    try:
        library = Library.objects.get(name="City Central Library")
        books = library.books.all()
        for book in books:
            print(f"  - {book.title}")
    except Library.DoesNotExist:
        print("  Library not found")
    
    # Approach 2: Using reverse relationship
    print("\nb) Using book.libraries.all() - reverse relationship:")
    book = Book.objects.first()
    if book:
        libraries = book.libraries.all()
        print(f"  Book '{book.title}' is in libraries:")
        for lib in libraries:
            print(f"  - {lib.name}")
    
    # 3. OneToOne relationships
    print("\n3. ONETOONE RELATIONSHIPS:")
    print("-" * 30)
    
    # Approach 1: Using Librarian.objects.get(library=library) - AS REQUESTED
    print("a) Using Librarian.objects.get(library=library):")
    try:
        library = Library.objects.get(name="City Central Library")
        librarian = Librarian.objects.get(library=library)
        print(f"  Librarian: {librarian.name}")
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        print("  Library or Librarian not found")
    
    # Approach 2: Using reverse relationship
    print("\nb) Using library.librarian (reverse relationship):")
    try:
        library = Library.objects.get(name="City Central Library")
        librarian = library.librarian
        print(f"  Librarian: {librarian.name}")
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        print("  Library or Librarian not found")
    
    # Approach 3: Using __ lookup
    print("\nc) Using Librarian.objects.get(library__name='City Central Library'):")
    try:
        librarian = Librarian.objects.get(library__name="City Central Library")
        print(f"  Librarian: {librarian.name}")
    except Librarian.DoesNotExist:
        print("  Librarian not found")

def create_sample_data():
    """
    Create sample data to test the queries
    """
    # Clear existing sample data to avoid duplicates
    Librarian.objects.all().delete()
    Library.objects.filter(name="City Central Library").delete()
    Book.objects.filter(author__name__in=["J.K. Rowling", "George Orwell"]).delete()
    Author.objects.filter(name__in=["J.K. Rowling", "George Orwell"]).delete()
    
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
    
    # Create additional data for comprehensive demonstration
    library2 = Library.objects.create(name="University Library")
    library2.books.add(book3, book4)
    Librarian.objects.create(name="Bob Smith", library=library2)
    
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
    
    # Query 2: List all books in a library
    print("\n2. List all books in a library:")
    list_all_books_in_library("City Central Library")
    
    # Query 3: Retrieve librarian for a library using Librarian.objects.get(library=...)
    print("\n3. Retrieve librarian for a library (using Librarian.objects.get(library=...)):")
    retrieve_librarian_for_library("City Central Library")
    
    # Query 3b: Alternative approach for comparison
    print("\n3b. Retrieve librarian (alternative approach):")
    retrieve_librarian_alternative("City Central Library")
    
    # Demonstrate all relationship queries comprehensively
    demonstrate_all_relationship_queries()
    
    # Show summary of all data
    print("\n" + "="*50)
    print("DATA SUMMARY")
    print("="*50)
    print(f"Authors: {Author.objects.count()}")
    print(f"Books: {Book.objects.count()}")
    print(f"Libraries: {Library.objects.count()}")
    print(f"Librarians: {Librarian.objects.count()}")
