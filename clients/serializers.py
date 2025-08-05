from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Client

User = get_user_model()

class ClientUserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ['id', 'nom', 'prenom', 'email', 'telephone', 'adresse', 'full_name']

class ClientSerializer(serializers.ModelSerializer):
    user = ClientUserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    nom_complet = serializers.ReadOnlyField()
    
    # Champs pour création d'utilisateur
    nom = serializers.CharField(write_only=True, required=False)
    prenom = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)
    telephone = serializers.CharField(write_only=True, required=False)
    adresse = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Client
        fields = ['id', 'user', 'user_id', 'numero_client', 'date_adhesion', 'statut', 
                 'nom_complet', 'created_at', 'updated_at',
                 'nom', 'prenom', 'email', 'telephone', 'adresse', 'password']
        read_only_fields = ['numero_client', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Extraire données utilisateur
        user_data = {}
        for field in ['nom', 'prenom', 'email', 'telephone', 'adresse']:
            if field in validated_data:
                user_data[field] = validated_data.pop(field)
        
        password = validated_data.pop('password', None)
        
        if 'user_id' in validated_data:
            user = User.objects.get(id=validated_data.pop('user_id'))
        elif user_data:
            user_data['role'] = 'client'
            user = User.objects.create_user(**user_data)
            if password:
                user.set_password(password)
                user.save()
        else:
            raise serializers.ValidationError("user_id ou données utilisateur requis")
        
        return Client.objects.create(user=user, **validated_data)
