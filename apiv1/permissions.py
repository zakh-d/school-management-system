from rest_framework.permissions import BasePermission


class HasSchoolPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.school is not None
