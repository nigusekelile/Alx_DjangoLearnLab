# relationship_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from .models import Book, Library, UserProfile, Author
from .forms import BookForm, CustomUserCreationForm

# Update registration view to use CustomUserCreationForm
def register_view(request):
    """
    User registration view using custom user model
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Assign role based on some logic or keep default 'Member'
            profile = user.profile
            profile.role = 'Member'  # Default role for new users
            profile.save()
            
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to the library system.')
            return redirect('relationship_app:list_books')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'relationship_app/register.html', {'form': form})

# Role-based access control functions
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Member'

# Role-based views
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

# Book Management Views with Custom Permissions
@login_required(login_url='/relationship/login/')
@permission_required('relationship_app.can_view_book', login_url='/relationship/login/')
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

@login_required(login_url='/relationship/login/')
@permission_required('relationship_app.can_add_book', login_url='/relationship/login/')
def add_book(request):
    """
    View to add a new book - requires can_add_book permission
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.created_by = request.user
            book.updated_by = request.user
            book.save()
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('relationship_app:list_books')
    else:
        form = BookForm()
    
    context = {
        'form': form,
        'action': 'Add',
    }
    return render(request, 'relationship_app/book_form.html', context)

@login_required(login_url='/relationship/login/')
@permission_required('relationship_app.can_change_book', login_url='/relationship/login/')
def edit_book(request, pk):
    """
    View to edit an existing book - requires can_change_book permission
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.updated_by = request.user
            book.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('relationship_app:list_books')
    else:
        form = BookForm(instance=book)
    
    context = {
        'form': form,
        'action': 'Edit',
        'book': book,
    }
    return render(request, 'relationship_app/book_form.html', context)

@login_required(login_url='/relationship/login/')
@permission_required('relationship_app.can_delete_book', login_url='/relationship/login/')
def delete_book(request, pk):
    """
    View to delete a book - requires can_delete_book permission
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" deleted successfully!')
        return redirect('relationship_app:list_books')
    
    context = {
        'book': book,
    }
    return render(request, 'relationship_app/book_confirm_delete.html', context)

# Class-based views with permissions
class LibraryDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Class-based view that displays details for a specific library
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    login_url = '/relationship/login/'
    permission_required = 'relationship_app.can_view_book'
    
    def get_queryset(self):
        return Library.objects.prefetch_related('books__author')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = self.request.user.profile.role if hasattr(self.request.user, 'profile') else 'No Role'
        return context

class LibraryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Class-based view that displays all libraries
    """
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'
    login_url = '/relationship/login/'
    permission_required = 'relationship_app.can_view_book'
    
    def get_queryset(self):
        return Library.objects.prefetch_related('books')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = self.request.user.profile.role if hasattr(self.request.user, 'profile') else 'No Role'
        return context
