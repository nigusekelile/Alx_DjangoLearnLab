from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from django.urls import reverse_lazy
from .models import Post, Profile
from .forms import (
    CustomUserCreationForm, 
    CustomAuthenticationForm, 
    UserUpdateForm, 
    ProfileUpdateForm,
    PostCreateForm
)

# Home View
def home(request):
    latest_posts = Post.objects.all().order_by('-published_date')[:3]
    return render(request, 'blog/home.html', {'latest_posts': latest_posts})

# Post List View
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 6  # Show 6 posts per page
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Blog Posts'
        return context

# Post Detail View
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add related posts
        context['related_posts'] = Post.objects.filter(
            author=self.object.author
        ).exclude(pk=self.object.pk)[:3]
        return context

# Post Create View
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        # Set the author to the current logged-in user
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Post'
        context['submit_text'] = 'Create Post'
        return context

# Post Update View
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        # Check if the current user is the author of the post
        post = self.get_object()
        return self.request.user == post.author
    
    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized to edit this post.')
        return redirect('post-detail', pk=self.kwargs.get('pk'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Post'
        context['submit_text'] = 'Update Post'
        return context

# Post Delete View
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        # Check if the current user is the author of the post
        post = self.get_object()
        return self.request.user == post.author
    
    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized to delete this post.')
        return redirect('post-detail', pk=self.kwargs.get('pk'))

# Keep function-based views for authentication (these can stay as they are)
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Account created for {username}! You are now logged in.')
                return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'blog/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile
        )
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'blog/profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('change-password')
        
        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
            return redirect('change-password')
        
        if len(new_password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('change-password')
        
        request.user.set_password(new_password1)
        request.user.save()
        login(request, request.user)
        messages.success(request, 'Your password has been changed successfully!')
        return redirect('profile')
    
    return render(request, 'blog/change_password.html')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView,
    FormView
)
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseForbidden
from .models import Post, Profile, Comment
from .forms import (
    CustomUserCreationForm, 
    CustomAuthenticationForm, 
    UserUpdateForm, 
    ProfileUpdateForm,
    PostCreateForm,
    CommentForm,
    CommentEditForm
)

# Existing views remain...

# Add to PostDetailView to include comments
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        
        # Get active comments for this post
        comments = post.comments.filter(active=True)
        
        # Add comment form to context
        context['comment_form'] = CommentForm()
        context['comments'] = comments
        context['comment_count'] = comments.count()
        context['related_posts'] = Post.objects.filter(
            author=post.author
        ).exclude(pk=post.pk)[:3]
        
        return context

# Comment Create View
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        
        messages.success(self.request, 'Your comment has been posted successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs['pk']}) + '#comments-section'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        context['title'] = 'Add a Comment'
        return context

# Comment Update View
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentEditForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Your comment has been updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        comment = self.get_object()
        return comment.can_edit(self.request.user)
    
    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized to edit this comment.')
        comment = self.get_object()
        return redirect('post-detail', pk=comment.post.pk)
    
    def get_success_url(self):
        comment = self.get_object()
        return reverse_lazy('post-detail', kwargs={'pk': comment.post.pk}) + f'#comment-{comment.pk}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object.post
        context['title'] = 'Edit Comment'
        context['editing'] = True
        return context

# Comment Delete View
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Your comment has been deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        comment = self.get_object()
        return comment.can_delete(self.request.user)
    
    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized to delete this comment.')
        comment = self.get_object()
        return redirect('post-detail', pk=comment.post.pk)
    
    def get_success_url(self):
        comment = self.get_object()
        return reverse_lazy('post-detail', kwargs={'pk': comment.post.pk}) + '#comments-section'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object.post
        return context

# AJAX Comment View (for real-time updates)
@login_required
def add_comment_ajax(request, pk):
    """Handle AJAX comment submission"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            
            # Return comment data for AJAX rendering
            return JsonResponse({
                'success': True,
                'comment_id': comment.pk,
                'author': comment.author.username,
                'author_url': comment.author.profile.profile_picture_url,
                'content': comment.content,
                'created_at': comment.get_time_since_created(),
                'edit_url': comment.get_edit_url(),
                'delete_url': comment.get_delete_url(),
                'can_edit': comment.can_edit(request.user),
                'can_delete': comment.can_delete(request.user),
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

# Function to handle inline comment submission (from post detail page)
@login_required
def add_comment(request, pk):
    """Handle comment submission from post detail page"""
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            
            messages.success(request, 'Your comment has been posted successfully!')
            return redirect('post-detail', pk=pk)
        else:
            # If form is invalid, we need to re-render the post detail page
            # with the form errors
            context = {
                'post': post,
                'comment_form': form,
                'comments': post.comments.filter(active=True),
                'comment_count': post.comments.filter(active=True).count(),
                'related_posts': Post.objects.filter(
                    author=post.author
                ).exclude(pk=post.pk)[:3],
            }
            return render(request, 'blog/post_detail.html', context)
    
    # If not POST, redirect to post detail
    return redirect('post-detail', pk=pk)

# The rest of the existing views remain unchanged...