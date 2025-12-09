from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the object.
        # Check if the object has an 'author' attribute
        if hasattr(obj, 'author'):
            return obj.author == request.user
        
        # For other objects, check if they have a 'user' attribute
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        
        # If the object doesn't have an author or user attribute, deny permission
        return False