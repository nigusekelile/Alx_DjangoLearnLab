# Delete

```python
from bookshelf.models import Book
b = Book.objects.get(title="Nineteen Eighty-Four")
b.delete()
list(Book.objects.all())

# Expected Output: 
# []
