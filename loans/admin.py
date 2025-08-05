from django.contrib import admin
from .models import Pret, Remboursement

@admin.register(Pret)
class PretAdmin(admin.ModelAdmin):
    list_display = ('get_client', 'montant', 'taux_interet', 'statut', 'date_octroi')
    list_filter = ('statut', 'date_octroi')
    search_fields = ('client__user__nom', 'client__numero_client')
    raw_id_fields = ('client', 'produit')
    
    def get_client(self, obj):
        return obj.client.nom_complet
    get_client.short_description = 'Client'

@admin.register(Remboursement)
class RemboursementAdmin(admin.ModelAdmin):
    list_display = ('reference', 'get_client', 'montant', 'date_paiement', 'mode_paiement')
    list_filter = ('mode_paiement', 'date_paiement')
    search_fields = ('reference', 'pret__client__user__nom')
    raw_id_fields = ('pret',)
    
    def get_client(self, obj):
        return obj.pret.client.nom_complet
    get_client.short_description = 'Client'
