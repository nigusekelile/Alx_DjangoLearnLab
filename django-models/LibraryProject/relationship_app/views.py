# relationship_app/views.py
from .models import Library
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book, Library  # Added Library import

# Function-based view to list all books
def list_books(request):
    """
    Function-based view that displays all books in the database
    """
    books = Book.objects.all().select_related('author')  # Optimize query with select_related
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display library details
class LibraryDetailView(DetailView):
    """
    Class-based view that displays details for a specific library
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_queryset(self):
        # Optimize query by prefetching related books and their authors
        return Library.objects.prefetch_related('books__author')

# Class-based view to list all libraries
class LibraryListView(ListView):
    """
    Class-based view that displays all libraries
    """
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'
    
    def get_queryset(self):
        # Optimize query by prefetching related books
        return Library.objects.prefetch_related('books')

