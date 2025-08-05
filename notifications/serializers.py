from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

class NotificationUserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ['id', 'nom', 'prenom', 'email', 'full_name']

class NotificationSerializer(serializers.ModelSerializer):
    user = NotificationUserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    type_action_display = serializers.CharField(source='get_type_action_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'user_id', 'type_action', 'type_action_display',
            'titre', 'description', 'priority', 'priority_display',
            'date_action', 'lu', 'date_lecture', 'is_global',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['date_lecture', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        if not attrs.get('is_global', False) and not attrs.get('user_id'):
            raise serializers.ValidationError(
                "Un utilisateur est requis pour les notifications non globales."
            )
        return attrs

class NotificationListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    type_action_display = serializers.CharField(source='get_type_action_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'user_name', 'type_action', 'type_action_display',
            'titre', 'priority', 'priority_display', 'date_action',
            'lu', 'is_global', 'created_at'
        ]
