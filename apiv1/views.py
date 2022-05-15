from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.models import CustomUser
from apiv1.permissions import HasSchoolPermission
from apiv1.serializers import ClassSerializer


class AvailableClassesListAPIView(ListAPIView):

    permission_classes = [IsAuthenticated, HasSchoolPermission]
    serializer_class = ClassSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == CustomUser.Roles.ADMIN_MEMBER:
            return user.school.classes.all()
        return user.classes.all()
