# Update

```python
from bookshelf.models import Book
b = Book.objects.get(title="1984")
b.title = "Nineteen Eighty-Four"
b.save()
Book.objects.get(id=b.id).title

# Expected Output:
# 'Nineteen Eighty-Four'
