# Retrieve

```python
from bookshelf.models import Book
books = Book.objects.all()
for b in books:
    print(b.id, b.title, b.author, b.publication_year)

# Expected Output:
# 1 1984 George Orwell 1949

# Or retrieve by title:

```python
b = Book.objects.get(title="1984")
b.id, b.title, b.author, b.publication_year

# Expected Output:
(1, '1984', 'George Orwell', 1949)
