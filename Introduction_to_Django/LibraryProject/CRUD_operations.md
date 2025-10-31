# Create

```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book

# Expected output
# <Book: 1984 by George Orwell (1949)>


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


# Update

```python
from bookshelf.models import Book
b = Book.objects.get(title="1984")
b.title = "Nineteen Eighty-Four"
b.save()
Book.objects.get(id=b.id).title

# Expected Output:
# 'Nineteen Eighty-Four'

# Delete

```python
from bookshelf.models import Book
b = Book.objects.get(title="Nineteen Eighty-Four")
b.delete()
list(Book.objects.all())

# Expected Output: 
# []
