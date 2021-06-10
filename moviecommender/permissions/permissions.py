from django.contrib.auth.models import Group
from rest_framework import permissions

from moviecommender.commons.permissions import AdminPermission


def _is_in_group(user, group_name):
    """
    Takes a user and a group name, and returns `True` if the user is in that group.
    """
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None


def _has_group_permission(user, required_groups):
    return any([_is_in_group(user, group_name) for group_name in required_groups])


class IsLoggedIn(permissions.BasePermission):

    required_groups = ['ADMIN', 'COMMON_USER', 'MOVIE_FILLER']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission

    def has_object_permission(self, request, view, obj):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        if self.required_groups is None:
            return False
        return obj == request.user or has_group_permission


class IsAdminUser(permissions.BasePermission):

    required_groups = ['ADMIN']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission or bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission or bool(request.user and request.user.is_staff)


class IsMovieFiller(permissions.BasePermission):

    required_groups = ['MOVIE_FILLER', 'ADMIN']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission
