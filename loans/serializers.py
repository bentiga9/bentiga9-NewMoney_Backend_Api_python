from rest_framework import serializers
from .models import Pret, Remboursement

class PretSerializer(serializers.ModelSerializer):
    client_nom = serializers.CharField(source='client.nom_complet', read_only=True)
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    montant_restant = serializers.ReadOnlyField()
    
    class Meta:
        model = Pret
        fields = ['id', 'client', 'client_nom', 'produit', 'produit_nom', 'montant',
                 'taux_interet', 'duree', 'date_octroi', 'date_fin',
                 'montant_total_a_rembourser', 'montant_rembourse', 'montant_restant',
                 'statut', 'statut_display', 'created_at', 'updated_at']
        read_only_fields = ['montant_total_a_rembourser', 'montant_rembourse']
    
    def validate_montant(self, value):
        if value <= 0:
            raise serializers.ValidationError("Le montant doit être positif")
        return value

class RemboursementSerializer(serializers.ModelSerializer):
    pret_client = serializers.CharField(source='pret.client.nom_complet', read_only=True)
    mode_paiement_display = serializers.CharField(source='get_mode_paiement_display', read_only=True)
    
    class Meta:
        model = Remboursement
        fields = ['id', 'pret', 'pret_client', 'montant', 'date_paiement',
                 'mode_paiement', 'mode_paiement_display', 'reference',
                 'justificatif_url', 'created_at', 'updated_at']
        read_only_fields = ['reference']
    
    def validate(self, attrs):
        pret = attrs.get('pret')
        montant = attrs.get('montant')
        
        if pret and montant:
            if montant > pret.montant_restant:
                raise serializers.ValidationError(
                    f"Montant supérieur au restant: {pret.montant_restant}"
                )
        return attrs
