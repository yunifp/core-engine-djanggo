from rest_framework import viewsets
from .models import ActivityLog
from .serializers import ActivityLogSerializer
from apps.accounts.permissions import HasDynamicPermission

class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.select_related('user').all().order_by('-created_at')
    serializer_class = ActivityLogSerializer
    permission_classes = [HasDynamicPermission] 