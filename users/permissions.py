from rest_framework.permissions import BasePermission

class UserPermissions(BasePermission):
    not_authenticated_methods = ['create', ]

    def has_permission(self, request, view):
        if view.action in self.not_authenticated_methods:
            return True

        if request.user.is_authenticated():
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated() and request.user == obj or request.user.is_superuser or request.user.has_perms('auth.change_user'):
            return True

        return False