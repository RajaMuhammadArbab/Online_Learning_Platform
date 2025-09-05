from rest_framework.permissions import BasePermission

class IsCourseOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        
        return bool(request.user and request.user.is_authenticated and (request.user.is_admin() or obj.created_by == request.user))
