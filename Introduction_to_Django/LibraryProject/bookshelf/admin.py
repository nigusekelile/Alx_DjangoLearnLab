from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Columns shown in the changelist (list view)
    list_display = ("id", "title", "author", "publication_year")

    # Allow quick filtering by these fields (right sidebar)
    list_filter = ("publication_year", "author")

    # Add search box that searches these fields
    search_fields = ("title", "author")

    # Allow inline editing of some fields from the list view
    list_editable = ("author", "publication_year")

    # Default ordering in the list view
    ordering = ("-publication_year", "title")

    # How many items per page
    list_per_page = 25

    # Optional: show only certain fields on the add/edit form and their layout
    # fields = ("title", "author", "publication_year")

    # Optional: add read-only fields (useful if you later add auto-generated fields)
    # readonly_fields = ()
