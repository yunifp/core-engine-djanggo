from rest_framework import permissions

class HasDynamicPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if not request.user.role:
            return False

        # 1. Jalur VVIP untuk Super Admin
        role_name = request.user.role.name.lower()
        if role_name == 'super admin' or role_name == 'superadmin':
            return True

        # 2. Ambil semua izin yang dimiliki user dari database
        user_permissions = request.user.role.permissions.values_list('name', flat=True)

        # 3. Ambil nama model/view secara dinamis (misal: 'employee', 'department')
        # view.basename biasanya berisi nama endpoint yang didaftarkan di router
        app_label = view.basename if hasattr(view, 'basename') else None
        
        if not app_label:
            return False

        # 4. Petakan method ke aksi (view, add, change, delete)
        method_mapping = {
            'GET': 'view',
            'POST': 'add',
            'PUT': 'change',
            'PATCH': 'change',
            'DELETE': 'delete'
        }
        action = method_mapping.get(request.method)

        # 5. Konstruksi nama permission secara dinamis
        # Contoh: can_view_employee, can_add_department, dll.
        required_permission = f"can_{action}_{app_label}"

        # 6. Cek apakah string ini ada di dalam daftar izin di database
        return required_permission in user_permissions