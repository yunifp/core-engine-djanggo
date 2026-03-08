from rest_framework import viewsets, filters  # <-- 'filters' wajib di-import di sini
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from .models import Department, Position
from .serializers import DepartmentSerializer, PositionSerializer
from apps.accounts.permissions import HasDynamicPermission

class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    permission_classes = [HasDynamicPermission]
    
    # Konfigurasi Search
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']

    def get_queryset(self):
        # Menghitung jumlah relasi employee yang terhubung ke departemen ini
        return Department.objects.annotate(employee_count=Count('employee')).order_by('name')


class PositionViewSet(viewsets.ModelViewSet):
    serializer_class = PositionSerializer
    permission_classes = [HasDynamicPermission]
    
    # Konfigurasi Search & Filter
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description', 'department__name']
    filterset_fields = ['department']

    def get_queryset(self):
        # Menghitung jumlah relasi employee yang terhubung ke posisi ini
        return Position.objects.annotate(employee_count=Count('employee')).order_by('name')