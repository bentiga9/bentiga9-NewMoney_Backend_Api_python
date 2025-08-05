# users/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema

from .models import User
from .serializers import UserSerializer, LoginSerializer, UserProfileSerializer

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des utilisateurs"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'login']:
            permission_classes = [AllowAny]
        elif self.action in ['list', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """Connexion utilisateur"""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserProfileSerializer(user).data,
                'message': 'Connexion réussie'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Déconnexion utilisateur"""
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Déconnexion réussie'})
        except Exception as e:
            return Response(
                {'error': 'Erreur lors de la déconnexion'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Profil utilisateur connecté"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
