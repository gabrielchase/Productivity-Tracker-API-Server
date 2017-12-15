from rest_framework import permissions


class ActivityPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        
        # If the object being viewed is the same as the request user
            # Return True
        return obj.user == request.user
