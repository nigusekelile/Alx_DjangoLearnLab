# check_books.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Book, Author

def check_books():
    print("📚 Checking books in database...")
    
    books = Book.objects.all().select_related('author')
    
    if books.exists():
        print(f"✅ Found {books.count()} books:")
        for book in books:
            print(f"   ID: {book.id} - '{book.title}' by {book.author.name}")
    else:
        print("❌ No books found in database")
        
    # Check authors too
    authors = Author.objects.all()
    print(f"\n✍️  Found {authors.count()} authors:")
    for author in authors:
        print(f"   - {author.name}")

if __name__ == "__main__":
    check_books()
