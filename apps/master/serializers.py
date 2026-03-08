from rest_framework import serializers
from .models import Department, Position

class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'employee_count']

class PositionSerializer(serializers.ModelSerializer):
    employee_count = serializers.IntegerField(read_only=True)
    department_detail = DepartmentSerializer(source='department', read_only=True) # Tambahan untuk Frontend

    class Meta:
        model = Position
        fields = ['id', 'department', 'department_detail', 'name', 'description', 'employee_count']