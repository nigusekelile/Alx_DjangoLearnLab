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
