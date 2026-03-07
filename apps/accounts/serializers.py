from rest_framework import serializers
from .models import User, Role, Permission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    permissions_detail = PermissionSerializer(source='permissions', many=True, read_only=True)
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'permissions', 'permissions_detail']

class UserSerializer(serializers.ModelSerializer):
    role_detail = RoleSerializer(source='role', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'role', 'role_detail', 'is_active']
        extra_kwargs = {'password': {'write_only': True}} 

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user