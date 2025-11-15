# Delete

```python
from bookshelf.models import Book

# Retrieve the book to delete
book = Book.objects.get(id=book.id)

# Delete the book
book.delete()

# Verify deletion
list(Book.objects.all())


# Expected Output: 
# []
