from rest_framework import serializers
from .models import Employee
from apps.accounts.serializers import UserSerializer

class EmployeeSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'user', 'user_detail', 'employee_id', 'department', 'position', 'salary', 'hire_date', 'created_at']