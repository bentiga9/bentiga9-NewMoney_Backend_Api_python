from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ['id', 'nom', 'prenom', 'email', 'telephone', 'adresse', 
                 'role', 'password', 'full_name', 'is_active', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if user and user.is_active:
                data['user'] = user
            else:
                raise serializers.ValidationError('Identifiants invalides')
        else:
            raise serializers.ValidationError('Email et mot de passe requis')
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ['id', 'nom', 'prenom', 'email', 'telephone', 'adresse', 
                 'role', 'full_name', 'is_active', 'date_joined']
        read_only_fields = ['email', 'role']

# ================================

# users/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import User
from .serializers import UserSerializer, LoginSerializer, UserProfileSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'login']:
            return [AllowAny()]
        elif self.action in ['list', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """Connexion utilisateur"""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserProfileSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Déconnexion utilisateur"""
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Déconnexion réussie'})
        except:
            return Response({'error': 'Erreur'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Profil utilisateur connecté"""
        return Response(UserProfileSerializer(request.user).data)
