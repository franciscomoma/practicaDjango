import datetime
from rest_framework.permissions import BasePermission

class BlogPermissions(BasePermission):
    not_authenticated_methods = ['list', ]

    def has_permission(self, request, view):
        if view.action in self.not_authenticated_methods:
            return True

        if request.user.is_authenticated():
            return True

        return False

class PostPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.blog.owner == request.user or request.user.is_superuser:
            return True

        if view.action == 'retrieve':
            if obj.publish_date < datetime.datetime.now():
                return True

        return False
