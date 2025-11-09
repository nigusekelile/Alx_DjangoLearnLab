# LibraryProject/urls.py (or your project's urls.py)
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('relationship/', include('relationship_app.urls')),
    
    # Redirect accounts/ URLs to relationship/ URLs
    path('accounts/login/', RedirectView.as_view(url='/relationship/login/', permanent=False)),
    path('accounts/logout/', RedirectView.as_view(url='/relationship/logout/', permanent=False)),
    path('accounts/', RedirectView.as_view(url='/relationship/', permanent=False)),
]
