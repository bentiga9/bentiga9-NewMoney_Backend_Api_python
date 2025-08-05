from rest_framework import serializers
from .models import Condition, Produit

class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ['id', 'nom', 'description', 'created_at', 'updated_at']

class ProduitSerializer(serializers.ModelSerializer):
    conditions = ConditionSerializer(read_only=True)
    conditions_id = serializers.IntegerField(write_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    duree_display = serializers.CharField(source='get_duree_display', read_only=True)
    
    class Meta:
        model = Produit
        fields = ['id', 'nom', 'description', 'type', 'type_display', 'taux_interet',
                 'frais', 'duree', 'duree_display', 'conditions', 'conditions_id',
                 'is_active', 'created_at', 'updated_at']