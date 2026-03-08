from rest_framework import permissions

class HasDynamicPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if not request.user.role:
            return False

        role_name = request.user.role.name.lower()
        if role_name in ['super admin', 'superadmin']:
            return True

        user_permissions = request.user.role.permissions.values_list('name', flat=True)

        app_label = view.basename if hasattr(view, 'basename') else None
        if not app_label:
            return False

        method_mapping = {
            'GET': 'view',
            'POST': 'add',
            'PUT': 'change',
            'PATCH': 'change',
            'DELETE': 'delete'
        }
        
        action = method_mapping.get(request.method)
        required_permission = f"can_{action}_{app_label}"

        return required_permission in user_permissions