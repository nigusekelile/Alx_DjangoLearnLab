"""
Custom permission classes for API application.
Provides fine-grained control over API endpoint access.
"""

from rest_framework import permissions

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Custom permission class that allows:
    - Read-only access to unauthenticated users (GET, HEAD, OPTIONS)
    - Full access to authenticated users (GET, POST, PUT, PATCH, DELETE)
    
    This is similar to DRF's built-in but with clearer documentation
    and potential for future customization.
    """
    
    def has_permission(self, request, view):
        """
        Check if user has permission to access the view.
        
        Args:
            request: The incoming request
            view: The target view
            
        Returns:
            bool: True if permission granted, False otherwise
        """
        # Allow safe methods (GET, HEAD, OPTIONS) for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only allow unsafe methods for authenticated users
        return request.user and request.user.is_authenticated

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission that only allows owners of an object to edit it.
    Read-only access is granted to all users.
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Check object-level permissions.
        
        Args:
            request: The incoming request
            view: The target view
            obj: The object being accessed
            
        Returns:
            bool: True if permission granted, False otherwise
        """
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner (if applicable)
        # This can be customized based on your model structure
        # For example, if books had an owner field:
        # return obj.owner == request.user
        
        # For now, return True for authenticated users (modify as needed)
        return request.user and request.user.is_authenticated