from rest_framework import permissions


class ActivityPermission(permissions.BasePermission):


    def has_permission(self, request, view):

        # Allow user registration
        if request.method == 'POST':
            return True
        
        # Don't allow users to get list of all activities
        # REFACTOR when groups and permissions are added
            # Only allow admin to see all users
        return view.kwargs.get('pk', False)

    def has_object_permission(self, request, view, obj):
        
        # If the object being viewed is the same as the request user
            # Return True
        return obj.user == request.user
