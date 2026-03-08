from rest_framework import serializers
from .models import Employee
from apps.accounts.serializers import UserSerializer
from apps.master.serializers import DepartmentSerializer, PositionSerializer

class EmployeeSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)
    department_detail = DepartmentSerializer(source='department', read_only=True) 
    position_detail = PositionSerializer(source='position', read_only=True)    

    class Meta:
        model = Employee
        fields = ['id', 'user', 'user_detail', 'employee_id', 
                  'department', 'department_detail', 
                  'position', 'position_detail', 
                  'salary', 'hire_date', 'created_at']