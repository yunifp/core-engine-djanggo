from rest_framework import permissions

class HasDynamicPermission(permissions.BasePermission):
    """
    Mengecek hak akses berdasarkan Method HTTP:
    GET = read, POST = create, PUT/PATCH = update, DELETE = delete
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if not request.user.role:
            return False
        if request.user.role.name == 'Super Admin':
            return True
        user_permissions = request.user.role.permissions.values_list('name', flat=True)
        method_mapping = {
            'GET': 'read',
            'POST': 'create',
            'PUT': 'update',
            'PATCH': 'update',
            'DELETE': 'delete'
        }
        required_permission = method_mapping.get(request.method)
        return required_permission in user_permissions