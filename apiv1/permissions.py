from rest_framework.permissions import BasePermission

from accounts.models import CustomUser


class HasSchoolPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.school is not None


class TeacherBelongsToClassOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        cls = view.get_object()
        if request.user.role == CustomUser.Roles.ADMIN_MEMBER:
            return request.user.school == cls.school
        return request.user in cls.teachers.all()


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == CustomUser.Roles.ADMIN_MEMBER
