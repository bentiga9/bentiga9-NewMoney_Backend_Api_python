from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Agent

User = get_user_model()

class AgentUserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ['id', 'nom', 'prenom', 'email', 'telephone', 'full_name']

class AgentSerializer(serializers.ModelSerializer):
    user = AgentUserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    nom_complet = serializers.ReadOnlyField()
    
    # Champs pour création
    nom = serializers.CharField(write_only=True, required=False)
    prenom = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)
    telephone = serializers.CharField(write_only=True, required=False)
    adresse = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Agent
        fields = ['id', 'user', 'user_id', 'statut', 'nom_complet', 'created_at',
                 'nom', 'prenom', 'email', 'telephone', 'adresse', 'password']
    
    def create(self, validated_data):
        user_data = {}
        for field in ['nom', 'prenom', 'email', 'telephone', 'adresse']:
            if field in validated_data:
                user_data[field] = validated_data.pop(field)
        
        password = validated_data.pop('password', None)
        
        if 'user_id' in validated_data:
            user = User.objects.get(id=validated_data.pop('user_id'))
        elif user_data:
            user_data['role'] = 'agent'
            user = User.objects.create_user(**user_data)
            if password:
                user.set_password(password)
                user.save()
        else:
            raise serializers.ValidationError("user_id ou données utilisateur requis")
        
        return Agent.objects.create(user=user, **validated_data)
