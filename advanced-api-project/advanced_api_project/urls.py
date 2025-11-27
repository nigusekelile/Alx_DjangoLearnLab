"""
Main URL configuration for advanced_api_project.
Includes API URLs and Django admin interface.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]