from rest_framework import serializers
from department.models import Department,Section

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name','description','url']

    

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['name','description','url']