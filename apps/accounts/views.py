from rest_framework import viewsets, filters
from .models import User, Role, Permission
from .serializers import UserSerializer, RoleSerializer, PermissionSerializer
from .permissions import HasDynamicPermission
from .pagination import DynamicPageSizePagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all().order_by('id')
    serializer_class = PermissionSerializer
    permission_classes = [HasDynamicPermission]
    pagination_class = DynamicPageSizePagination
    
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by('id')
    serializer_class = RoleSerializer
    permission_classes = [HasDynamicPermission]
    pagination_class = DynamicPageSizePagination
    
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related('role').all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [HasDynamicPermission]
    pagination_class = DynamicPageSizePagination
    
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email', 'role__name']

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        permissions_list = []
        
        if user.role:
            role_name = user.role.name.lower()
            if role_name in ['super admin', 'superadmin', 'admin']:
                permissions_list = list(Permission.objects.values_list('name', flat=True))
            else:
                permissions_list = list(user.role.permissions.values_list('name', flat=True))
                
        response_data = serializer.data
        response_data['permissions'] = permissions_list
        return Response(response_data)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token wajib disertakan"}, status=400)
                
            token = RefreshToken(refresh_token)
            token.blacklist() 
            return Response({"message": "Logout berhasil."}, status=205)
        except Exception:
            return Response({"error": "Token tidak valid."}, status=400)