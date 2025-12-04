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
    FormView,
    TemplateView
)
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Profile, Comment, Tag
from .forms import (
    CustomUserCreationForm, 
    CustomAuthenticationForm, 
    UserUpdateForm, 
    ProfileUpdateForm,
    PostCreateForm,
    CommentForm,
    CommentEditForm,
    SearchForm
)

# Home View - Updated with popular tags
def home(request):
    latest_posts = Post.objects.all().order_by('-published_date')[:3]
    popular_tags = Tag.get_popular_tags(limit=10)
    
    context = {
        'latest_posts': latest_posts,
        'popular_tags': popular_tags,
        'search_form': SearchForm(),
    }
    return render(request, 'blog/home.html', context)

# Post List View - Updated with tags
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by tag if provided
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags=tag)
        
        # Order by published date (newest first)
        return queryset.order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Blog Posts'
        
        # Add popular tags to context
        context['popular_tags'] = Tag.get_popular_tags(limit=10)
        context['search_form'] = SearchForm()
        
        # Check if filtering by tag
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            context['title'] = f'Posts tagged "{tag.name}"'
            context['current_tag'] = tag
        
        return context

# Post Detail View - Updated with tags and related posts
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
        
        # Get related posts based on tags and author
        context['related_posts'] = post.get_related_posts()
        
        # Add popular tags
        context['popular_tags'] = Tag.get_popular_tags(limit=10)
        context['search_form'] = SearchForm()
        
        return context

# Tag List View
class TagListView(ListView):
    model = Tag
    template_name = 'blog/tag_list.html'
    context_object_name = 'tags'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Annotate with post count
        queryset = queryset.annotate(post_count=Count('posts')).order_by('-post_count')
        
        # Search functionality for tags
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Tags'
        context['search_form'] = SearchForm()
        return context

# Posts by Tag View
class PostsByTagView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        tag_slug = self.kwargs['slug']
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        return Post.objects.filter(tags=self.tag).order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Posts tagged "{self.tag.name}"'
        context['current_tag'] = self.tag
        context['popular_tags'] = Tag.get_popular_tags(limit=10)
        context['search_form'] = SearchForm()
        return context

# Search View
class SearchView(FormView):
    template_name = 'blog/search_results.html'
    form_class = SearchForm
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET)
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        query = form.cleaned_data['q']
        search_in = form.cleaned_data['search_in']
        sort_by = form.cleaned_data['sort_by']
        
        # Start with all posts
        posts = Post.objects.all()
        
        # Apply search filters if query exists
        if query:
            search_filters = Q()
            
            if 'title' in search_in:
                search_filters |= Q(title__icontains=query)
            
            if 'content' in search_in:
                search_filters |= Q(content__icontains=query)
            
            if 'tags' in search_in:
                search_filters |= Q(tags__name__icontains=query)
            
            posts = posts.filter(search_filters).distinct()
        
        # Apply sorting
        if sort_by == 'date_new':
            posts = posts.order_by('-published_date')
        elif sort_by == 'date_old':
            posts = posts.order_by('published_date')
        elif sort_by == 'title_asc':
            posts = posts.order_by('title')
        elif sort_by == 'title_desc':
            posts = posts.order_by('-title')
        elif sort_by == 'relevance' and query:
            # For relevance, we could implement more sophisticated ranking
            # For now, we'll just sort by date (newest first)
            posts = posts.order_by('-published_date')
        else:
            posts = posts.order_by('-published_date')
        
        # Pagination
        paginator = Paginator(posts, 6)
        page = self.request.GET.get('page', 1)
        
        try:
            posts_page = paginator.page(page)
        except PageNotAnInteger:
            posts_page = paginator.page(1)
        except EmptyPage:
            posts_page = paginator.page(paginator.num_pages)
        
        context = self.get_context_data(
            form=form,
            query=query,
            posts=posts_page,
            search_in=search_in,
            sort_by=sort_by,
            result_count=posts.count()
        )
        
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search Results'
        context['popular_tags'] = Tag.get_popular_tags(limit=10)
        return context

# AJAX Tag Suggestions View
@login_required
def tag_suggestions(request):
    """Return JSON list of tag suggestions for autocomplete"""
    query = request.GET.get('q', '')
    
    if query:
        tags = Tag.objects.filter(name__icontains=query)[:10]
        suggestions = [{'id': tag.id, 'name': tag.name} for tag in tags]
    else:
        suggestions = []
    
    return JsonResponse({'suggestions': suggestions})

# The rest of existing views remain unchanged...
# [PostCreateView, PostUpdateView, PostDeleteView, Comment views, Authentication views]