# relationship_app/urls.py
from .views import list_books
from django.urls import path
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # Function-based view URL
    path('books/', views.list_books, name='list_books'),
    
    # Class-based view URLs
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('libraries/', views.LibraryListView.as_view(), name='library_list'),
]

# Authenticatio script 
# relationship_app/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # Authentication URLs
    path('login/', 
         LoginView.as_view(template_name='relationship_app/login.html'), 
         name='login'),
    
    # Use custom logout view that handles GET requests
    path('logout/', views.logout_view, name='logout'),
    
    path('register/', views.register_view, name='register'),
    
    # Book and Library URLs
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('libraries/', views.LibraryListView.as_view(), name='library_list'),
]
