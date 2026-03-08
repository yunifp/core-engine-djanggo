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
    
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        # 2. Pastikan 'permissions' dimasukkan ke dalam daftar fields
        fields = [
            'id', 'email', 'first_name', 'last_name', 
            'password', 'role', 'role_detail', 'is_active', 
            'permissions'
        ]
        extra_kwargs = {'password': {'write_only': True}} 

    # 3. Fungsi ini akan otomatis mengekstrak nama (name) dari relasi permission
    def get_permissions(self, obj):
        if obj.role and obj.role.permissions.exists():
            return list(obj.role.permissions.values_list('name', flat=True))
        return []

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user