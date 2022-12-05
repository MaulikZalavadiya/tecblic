from rest_framework import permissions


class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user

class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.user_type == 'Admin'