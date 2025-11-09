# relationship_app/views.py
from .models import Library
from django.views.generic.detail import DetailView
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

# Authentication Views
# relationship_app/views.py
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Book, Library

# Authentication Views
def login_view(request):
    """
    User login view
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('relationship_app:list_books')
    else:
        form = AuthenticationForm()
    
    return render(request, 'relationship_app/login.html', {'form': form})

def logout_view(request):
    """
    User logout view
    """
    logout(request)
    return render(request, 'relationship_app/logout.html')

def register_view(request):
    """
    User registration view
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app:list_books')
    else:
        form = UserCreationForm()
    
    return render(request, 'relationship_app/register.html', {'form': form})

# Update existing views to require authentication
@login_required
def list_books(request):
    """
    Function-based view that displays all books in the database
    """
    books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(LoginRequiredMixin, DetailView):
    """
    Class-based view that displays details for a specific library
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_queryset(self):
        return Library.objects.prefetch_related('books__author')

class LibraryListView(LoginRequiredMixin, ListView):
    """
    Class-based view that displays all libraries
    """
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'
    
    def get_queryset(self):
        return Library.objects.prefetch_related('books')
