import datetime
from rest_framework.permissions import BasePermission


class PostPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.blog.owner == request.user or request.user.is_superuser:
            return True

        if view.action == 'retrieve':
            if obj.publish_date < datetime.datetime.now():
                return True

        return False
