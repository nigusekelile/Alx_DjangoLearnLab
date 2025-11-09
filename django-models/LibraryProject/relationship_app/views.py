# Create your views here.
# relationship_app/views.py
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book, Library

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all().select_related('author')  # Optimize query
    return render(request, 'relationship_app/list_books.html', {'books': books})

# relationship_app/views.py (continued)
# Class-based view to display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_queryset(self):
        # Optimize query by prefetching related books and their authors
        return Library.objects.prefetch_related('books__author')

# Optional: Class-based view to list all libraries
class LibraryListView(ListView):
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'
