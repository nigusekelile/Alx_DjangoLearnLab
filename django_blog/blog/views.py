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
from taggit.models import Tag
from .models import Post, Profile, Comment
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

# Home View
def home(request):
    latest_posts = Post.objects.all().order_by('-published_date')[:3]
    
    # Get popular tags using taggit
    from .utils import get_popular_tags
    popular_tags = get_popular_tags(limit=10)
    
    context = {
        'latest_posts': latest_posts,
        'popular_tags': popular_tags,
        'search_form': SearchForm(),
    }
    return render(request, 'blog/home.html', context)

# Post List View
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
        from .utils import get_popular_tags
        context['popular_tags'] = get_popular_tags(limit=10)
        context['search_form'] = SearchForm()
        
        # Check if filtering by tag
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            context['title'] = f'Posts tagged "{tag.name}"'
            context['current_tag'] = tag
        
        return context

# Post Detail View
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
        from .utils import get_popular_tags
        context['popular_tags'] = get_popular_tags(limit=10)
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
        from django.db.models import Count
        queryset = queryset.annotate(
            post_count=Count('taggit_taggeditem_items')
        ).order_by('-post_count')
        
        # Search functionality for tags
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        
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
        from .utils import get_popular_tags
        context['popular_tags'] = get_popular_tags(limit=10)
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
        from .utils import get_popular_tags
        context['popular_tags'] = get_popular_tags(limit=10)
        return context

# AJAX Tag Suggestions View
@login_required
def tag_suggestions(request):
    """Return JSON list of tag suggestions for autocomplete"""
    query = request.GET.get('q', '')
    
    if query:
        tags = Tag.objects.filter(name__icontains=query)[:10]
        suggestions = [{'id': tag.id, 'name': tag.name, 'slug': tag.slug} for tag in tags]
    else:
        suggestions = []
    
    return JsonResponse({'suggestions': suggestions})

# Tag Cloud View
def tag_cloud(request):
    """Display tag cloud"""
    from .utils import get_tag_cloud
    tag_cloud_data = get_tag_cloud(min_count=1, max_count=50)
    
    context = {
        'tag_cloud': tag_cloud_data,
        'title': 'Tag Cloud',
        'search_form': SearchForm(),
    }
    return render(request, 'blog/tag_cloud.html', context)

# The rest of existing views remain unchanged...
# [PostCreateView, PostUpdateView, PostDeleteView, Comment views, Authentication views]