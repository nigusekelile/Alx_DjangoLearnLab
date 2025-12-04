from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile, Post, Comment
from taggit.models import Tag

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
                'placeholder': f'Enter your {field_name}'
            })

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us something about yourself...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            if field_name != 'bio':
                self.fields[field_name].widget.attrs.update({
                    'class': 'form-control'
                })

class PostCreateForm(forms.ModelForm):
    # django-taggit automatically handles tags through the model
    # We'll use a custom widget for better UX
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post content here...',
                'rows': 10
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tags separated by commas (e.g., django, python, web)',
                'data-role': 'tagsinput',
                'id': 'id_tags'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add help text for tags field
        self.fields['tags'].help_text = "Separate tags with commas"
        
        # If editing existing post, format tags as string
        if self.instance and self.instance.pk:
            tags_string = ', '.join(tag.name for tag in self.instance.tags.all())
            self.initial['tags'] = tags_string
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('Title must be at least 5 characters long.')
        return title
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 20:
            raise forms.ValidationError('Content must be at least 20 characters long.')
        return content

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 4,
                'maxlength': '1000',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = ''
        self.fields['content'].widget.attrs.update({
            'oninput': 'updateCharCounter(this)'
        })
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 5:
            raise forms.ValidationError('Comment must be at least 5 characters long.')
        if len(content) > 1000:
            raise forms.ValidationError('Comment cannot exceed 1000 characters.')
        return content

class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'maxlength': '1000',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = 'Edit your comment'
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 5:
            raise forms.ValidationError('Comment must be at least 5 characters long.')
        if len(content) > 1000:
            raise forms.ValidationError('Comment cannot exceed 1000 characters.')
        return content

class SearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search posts by title, content, or tags...',
            'aria-label': 'Search'
        })
    )
    
    search_in = forms.MultipleChoiceField(
        required=False,
        choices=[
            ('title', 'Title'),
            ('content', 'Content'),
            ('tags', 'Tags'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'search-options'
        }),
        initial=['title', 'content', 'tags']
    )
    
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ('relevance', 'Relevance'),
            ('date_new', 'Date (Newest)'),
            ('date_old', 'Date (Oldest)'),
            ('title_asc', 'Title (A-Z)'),
            ('title_desc', 'Title (Z-A)'),
        ],
        initial='relevance',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )