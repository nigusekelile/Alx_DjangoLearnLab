# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our ViewSet
router = DefaultRouter()
router.register(r'books_all', views.BookViewSet, basename='book_all')

# The API URLs are now determined automatically by the router
urlpatterns = [
    # Route for the BookList view (ListAPIView) - read-only
    path('books/', views.BookList.as_view(), name='book-list'),
    
    # Include the router URLs for BookViewSet (all CRUD operations)
    path('', include(router.urls)),
]