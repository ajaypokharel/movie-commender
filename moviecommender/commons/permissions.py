from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission

from moviecommender.user.constants import ADMIN


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            try:
                admin_group = Group.objects.get(user=request.user.id)
            except Group.DoesNotExist:
                admin_group = None
            if admin_group:
                if admin_group.name == ADMIN:
                    return True
        return False
