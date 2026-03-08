from rest_framework import viewsets
from .models import User, Role, Permission
from .serializers import UserSerializer, RoleSerializer, PermissionSerializer
from .permissions import HasDynamicPermission
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [HasDynamicPermission]

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [HasDynamicPermission]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related('role').all()
    serializer_class = UserSerializer
    permission_classes = [HasDynamicPermission]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Endpoint khusus untuk Frontend (GET /api/accounts/users/me/).
        Mengembalikan data profil user yang sedang login beserta daftar permission-nya.
        """
        user = request.user
        serializer = self.get_serializer(user)
        permissions_list = []
        role_name = None
        
        if user.role:
            role_name = user.role.name
            
            # BYPASS SUPERADMIN: Jika rolenya Superadmin, berikan SEMUA permission yang ada di sistem
            if role_name.lower() == 'superadmin':
                permissions_list = list(Permission.objects.values_list('name', flat=True))
            else:
                permissions_list = list(user.role.permissions.values_list('name', flat=True))
                
        response_data = serializer.data
        response_data['frontend_sidebar_access'] = permissions_list
        response_data['role_name'] = role_name

        return Response(response_data)
    
class LogoutAPIView(APIView):
        """
        Endpoint untuk menghancurkan (blacklist) Refresh Token.
        """
        permission_classes = [IsAuthenticated]

        def post(self, request):
            try:
                refresh_token = request.data.get("refresh")
                if not refresh_token:
                    return Response({"error": "Refresh token wajib disertakan"}, status=status.HTTP_400_BAD_REQUEST)
                    
                token = RefreshToken(refresh_token)
                token.blacklist() 
                return Response({"message": "Logout berhasil. Token telah dihancurkan."}, status=status.HTTP_205_RESET_CONTENT)
            except Exception as e:
                return Response({"error": "Token tidak valid atau sudah kadaluarsa."}, status=status.HTTP_400_BAD_REQUEST)
            