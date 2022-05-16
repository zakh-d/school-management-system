from rest_framework.permissions import BasePermission

from accounts.models import CustomUser


class HasSchoolPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.school is not None


class TeacherBelongsToClassOrIsAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.role == CustomUser.Roles.ADMIN_MEMBER:
            return request.user.school == obj.school
        return request.user in obj.teachers.all()
