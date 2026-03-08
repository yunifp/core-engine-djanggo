from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Employee
from .serializers import EmployeeSerializer
from apps.accounts.permissions import HasDynamicPermission
from apps.core.models import ActivityLog
from apps.notifications.models import Notification

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related('user', 'department', 'position').order_by('-created_at')
    
    serializer_class = EmployeeSerializer
    permission_classes = [HasDynamicPermission]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    
    search_fields = [
        'employee_id', 
        'user__first_name', 
        'user__last_name', 
        'user__email',
        'department__name', 
        'position__name'    
    ]
    
    filterset_fields = ['department', 'position']
    ordering_fields = ['salary', 'hire_date', 'created_at']

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return self.request.META.get('REMOTE_ADDR')

    def perform_create(self, serializer):
        employee = serializer.save()
        ActivityLog.objects.create(
            user=self.request.user,
            action="CREATE",
            description=f"Menambahkan data karyawan: {employee.employee_id}",
            ip_address=self.get_client_ip()
        )
        
        Notification.objects.create(
            user=employee.user,
            title="Selamat Datang!",
            message="Profil karyawan Anda telah ditambahkan ke sistem."
        )

    def perform_update(self, serializer):
        employee = serializer.save()
        
        ActivityLog.objects.create(
            user=self.request.user,
            action="UPDATE",
            description=f"Memperbarui data karyawan: {employee.employee_id}",
            ip_address=self.get_client_ip()
        )
        
        Notification.objects.create(
            user=employee.user,
            title="Pembaruan Data",
            message="Data profil Anda baru saja diperbarui oleh sistem."
        )

    def perform_destroy(self, instance):
        emp_id = instance.employee_id
        
        ActivityLog.objects.create(
            user=self.request.user,
            action="DELETE",
            description=f"Menghapus data karyawan: {emp_id}",
            ip_address=self.get_client_ip()
        )
        instance.delete()