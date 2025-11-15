# Django Admin configuration for `bookshelf.Book`

## File: bookshelf/admin.py

```python
from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "publication_year")
    list_filter = ("publication_year", "author")
    search_fields = ("title", "author")
    list_editable = ("author", "publication_year")
    ordering = ("-publication_year", "title")
    list_per_page = 25
