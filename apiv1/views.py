from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.models import CustomUser
from apiv1.permissions import HasSchoolPermission, TeacherBelongsToClassOrIsAdmin, IsAdmin
from apiv1.serializers import ClassSerializer, StudentSerializer, UserSerializer, SchoolUpdateSerializer
from school.models import Class


class AvailableClassesListAPIView(ListAPIView):

    permission_classes = [IsAuthenticated, HasSchoolPermission]
    serializer_class = ClassSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == CustomUser.Roles.ADMIN_MEMBER:
            return user.school.classes.all()
        return user.classes.all()


class StudentsFromClassAPIView(ListAPIView):

    permission_classes = [IsAuthenticated, TeacherBelongsToClassOrIsAdmin]
    serializer_class = StudentSerializer

    def get_object(self):
        return get_object_or_404(Class, id=self.kwargs.get('class_id'))

    def get_queryset(self):
        _class = self.get_object()
        return _class.students.all().order_by('order_in_class')


class MyInfoAPIView(RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class SchoolUpdateAPIView(UpdateAPIView):

    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = SchoolUpdateSerializer

    def get_object(self):
        return self.request.user.school
