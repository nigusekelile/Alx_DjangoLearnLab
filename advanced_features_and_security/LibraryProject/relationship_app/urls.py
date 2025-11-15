# relationship_app/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # Authentication URLs
    path('login/', 
         LoginView.as_view(
             template_name='relationship_app/login.html',
             redirect_authenticated_user=True
         ), 
         name='login'),
    
    path('logout/', 
         LogoutView.as_view(
             template_name='relationship_app/logout.html',
             next_page='/relationship/login/'
         ), 
         name='logout'),
    
    path('register/', views.register_view, name='register'),
    
    # Role-based views URLs
    path('admin/dashboard/', views.admin_view, name='admin_view'),
    path('librarian/dashboard/', views.librarian_view, name='librarian_view'),
    path('member/dashboard/', views.member_view, name='member_view'),
    
    # Book Management URLs with permissions
    path('books/', views.list_books, name='list_books'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
    
    # Library URLs
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('libraries/', views.LibraryListView.as_view(), name='library_list'),
    
    # Home page redirect
    path('', views.list_books, name='home'),
]
