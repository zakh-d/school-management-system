from rest_framework import serializers

from accounts.models import CustomUser
from school.models import Class, School
from student.models import Student


class ClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = Class
        fields = ('id', 'name')


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ('id', 'order_in_class', 'first_name', 'last_name')


class UserSerializer(serializers.ModelSerializer):

    role = serializers.SerializerMethodField()
    school = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'role', 'school')

    def get_role(self, obj):
        return obj.get_role_display()

    def get_school(self, obj):
        return obj.school.name


class SchoolUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ('name', )
