# relationship_app/views.py
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .models import Book, Library, UserProfile

# Role-based access control functions
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Member'

# Role-based views with proper authentication
@login_required(login_url='/relationship/login/')
@user_passes_test(is_admin, login_url='/relationship/login/')
def admin_view(request):
    """
    Admin view - only accessible by users with Admin role
    """
    users = UserProfile.objects.all().select_related('user')
    libraries = Library.objects.all()
    context = {
        'users': users,
        'libraries': libraries,
        'total_books': Book.objects.count(),
    }
    return render(request, 'relationship_app/admin_view.html', context)

@login_required(login_url='/relationship/login/')
@user_passes_test(is_librarian, login_url='/relationship/login/')
def librarian_view(request):
    """
    Librarian view - only accessible by users with Librarian role
    """
    libraries = Library.objects.all()
    books = Book.objects.all().select_related('author')
    context = {
        'libraries': libraries,
        'books': books,
        'available_books': Book.objects.count(),
    }
    return render(request, 'relationship_app/librarian_view.html', context)

@login_required(login_url='/relationship/login/')
@user_passes_test(is_member, login_url='/relationship/login/')
def member_view(request):
    """
    Member view - only accessible by users with Member role
    """
    books = Book.objects.all().select_related('author')
    libraries = Library.objects.all()
    context = {
        'books': books,
        'libraries': libraries,
        'user_books_borrowed': 0,
    }
    return render(request, 'relationship_app/member_view.html', context)

# Update other views to specify login URL
@login_required(login_url='/relationship/login/')
def list_books(request):
    """
    Function-based view that displays all books in the database
    """
    books = Book.objects.all().select_related('author')
    user_role = request.user.profile.role if hasattr(request.user, 'profile') else 'No Role'
    
    context = {
        'books': books,
        'user_role': user_role,
    }
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(LoginRequiredMixin, DetailView):
    """
    Class-based view that displays details for a specific library
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    login_url = '/relationship/login/'
    
    def get_queryset(self):
        return Library.objects.prefetch_related('books__author')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = self.request.user.profile.role if hasattr(self.request.user, 'profile') else 'No Role'
        return context

class LibraryListView(LoginRequiredMixin, ListView):
    """
    Class-based view that displays all libraries
    """
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'
    login_url = '/relationship/login/'
    
    def get_queryset(self):
        return Library.objects.prefetch_related('books')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = self.request.user.profile.role if hasattr(self.request.user, 'profile') else 'No Role'
        return context

# Registration view remains the same
def register_view(request):
    """
    User registration view with role selection
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Assign role based on some logic or keep default 'Member'
            profile = user.profile
            profile.role = 'Member'  # Default role for new users
            profile.save()
            
            login(request, user)
            return redirect('relationship_app:list_books')
    else:
        form = UserCreationForm()
    
    return render(request, 'relationship_app/register.html', {'form': form})
