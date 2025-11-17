# LibraryProject/bookshelf/views.py
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import CustomUser
from django.http import HttpResponseForbidden

# Function-based views with permission decorators
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def user_list_view(request):
    """View to list all users - requires can_view permission"""
    users = CustomUser.objects.all()
    return render(request, 'bookshelf/user_list.html', {'users': users})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def user_create_view(request):
    """View to create a new user - requires can_create permission"""
    if request.method == 'POST':
        # Handle form submission
        # This is a simplified example - in reality, you'd use a form
        pass
    return render(request, 'bookshelf/user_form.html')

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def user_edit_view(request, user_id):
    """View to edit a user - requires can_edit permission"""
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Additional check: users can edit their own profile without special permission
    if user != request.user and not request.user.has_perm('bookshelf.can_edit'):
        return HttpResponseForbidden("You don't have permission to edit other users' profiles")
    
    if request.method == 'POST':
        # Handle form submission
        pass
    return render(request, 'bookshelf/user_form.html', {'user': user})

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def user_delete_view(request, user_id):
    """View to delete a user - requires can_delete permission"""
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Prevent users from deleting themselves
    if user == request.user:
        return HttpResponseForbidden("You cannot delete your own account")
    
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'bookshelf/user_confirm_delete.html', {'user': user})

# Class-based views with permission mixins
class UserListView(PermissionRequiredMixin, ListView):
    """Class-based view to list users - requires can_view permission"""
    model = CustomUser
    template_name = 'bookshelf/user_list.html'
    context_object_name = 'users'
    permission_required = 'bookshelf.can_view'

class UserCreateView(PermissionRequiredMixin, CreateView):
    """Class-based view to create users - requires can_create permission"""
    model = CustomUser
    template_name = 'bookshelf/user_form.html'
    fields = ['username', 'email', 'date_of_birth', 'first_name', 'last_name']
    success_url = reverse_lazy('user_list')
    permission_required = 'bookshelf.can_create'

class UserUpdateView(PermissionRequiredMixin, UpdateView):
    """Class-based view to update users - requires can_edit permission"""
    model = CustomUser
    template_name = 'bookshelf/user_form.html'
    fields = ['username', 'email', 'date_of_birth', 'first_name', 'last_name', 'bio', 'phone_number']
    success_url = reverse_lazy('user_list')
    permission_required = 'bookshelf.can_edit'

class UserDeleteView(PermissionRequiredMixin, DeleteView):
    """Class-based view to delete users - requires can_delete permission"""
    model = CustomUser
    template_name = 'bookshelf/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')
    permission_required = 'bookshelf.can_delete'
    
    def dispatch(self, request, *args, **kwargs):
        # Prevent users from deleting themselves
        if self.get_object() == request.user:
            return HttpResponseForbidden("You cannot delete your own account")
        return super().dispatch(request, *args, **kwargs)
