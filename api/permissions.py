from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission:
    - Allow read-only access for any request
    - Allow write access only for admin users
    """
    
    def has_permission(self, request, view):
        # Allow GET, HEAD, OPTIONS requests
        if request.method in SAFE_METHODS:
            return True
        
        # Allow write permissions only for admin users
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission:
    - Allow access only for object owner or admin
    """
    
    def has_object_permission(self, request, view, obj):
        # Allow admin users
        if request.user and request.user.is_staff:
            return True
        
        # Check if the user is the owner of the object
        # Assuming the object has a 'user' attribute
        if hasattr(obj, 'user'):
            return obj.user == request.user
            
        # If the object is a User model instance
        if hasattr(obj, 'username'):
            return obj == request.user
            
        return False