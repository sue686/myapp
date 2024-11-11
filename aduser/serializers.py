from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['campus', 'name', 'path','givenname','surname','samaccountname','displayname', 'password', 'email']