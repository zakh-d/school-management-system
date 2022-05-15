from rest_framework import serializers

from school.models import Class


class ClassSerializer(serializers.ModelSerializer):

    class Meta:

        model = Class
        fields = ('id', 'name')
