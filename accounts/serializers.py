from rest_framework import serializers
from django.db import transaction
from .models import Compte, Transaction, Epargne

class CompteSerializer(serializers.ModelSerializer):
    client_nom = serializers.CharField(source='client.nom_complet', read_only=True)
    type_compte_display = serializers.CharField(source='get_type_compte_display', read_only=True)
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    
    class Meta:
        model = Compte
        fields = ['id', 'client', 'client_nom', 'numero_compte', 'type_compte', 
                 'type_compte_display', 'solde', 'date_ouverture', 'statut', 
                 'statut_display', 'created_at', 'updated_at']
        read_only_fields = ['numero_compte']

class TransactionSerializer(serializers.ModelSerializer):
    compte_numero = serializers.CharField(source='compte.numero_compte', read_only=True)
    type_transaction_display = serializers.CharField(source='get_type_transaction_display', read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'compte', 'compte_numero', 'type_transaction', 
                 'type_transaction_display', 'montant', 'date_transaction', 
                 'reference', 'description', 'solde_apres', 'created_at']
        read_only_fields = ['reference', 'solde_apres']
    
    def create(self, validated_data):
        compte = validated_data['compte']
        type_transaction = validated_data['type_transaction']
        montant = validated_data['montant']
        
        with transaction.atomic():
            if type_transaction in ['depot', 'virement']:
                compte.solde += montant
            elif type_transaction in ['retrait', 'transfert']:
                if compte.solde < montant:
                    raise serializers.ValidationError("Solde insuffisant")
                compte.solde -= montant
            
            compte.save()
            validated_data['solde_apres'] = compte.solde
            return Transaction.objects.create(**validated_data)

class EpargneSerializer(serializers.ModelSerializer):
    compte_numero = serializers.CharField(source='compte.numero_compte', read_only=True)
    periode_display = serializers.CharField(source='get_periode_display', read_only=True)
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    
    class Meta:
        model = Epargne
        fields = ['id', 'compte', 'compte_numero', 'montant', 'taux_interet', 
                 'periode', 'periode_display', 'date_epargne', 'montant_a_percevoir',
                 'date_debut_epargne', 'date_fin_epargne', 'statut', 'statut_display',
                 'created_at', 'updated_at']