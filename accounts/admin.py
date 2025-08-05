from django.contrib import admin
from .models import Compte, Transaction, Epargne

@admin.register(Compte)
class CompteAdmin(admin.ModelAdmin):
    list_display = ('numero_compte', 'get_client', 'type_compte', 'solde', 'statut')
    list_filter = ('type_compte', 'statut')
    search_fields = ('numero_compte', 'client__user__nom')
    raw_id_fields = ('client',)
    
    def get_client(self, obj):
        return obj.client.nom_complet
    get_client.short_description = 'Client'

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('reference', 'get_compte', 'type_transaction', 'montant', 'date_transaction')
    list_filter = ('type_transaction',)
    search_fields = ('reference', 'compte__numero_compte')
    raw_id_fields = ('compte',)
    
    def get_compte(self, obj):
        return obj.compte.numero_compte
    get_compte.short_description = 'Compte'

@admin.register(Epargne)
class EpargneAdmin(admin.ModelAdmin):
    list_display = ('get_compte', 'montant', 'periode', 'statut', 'date_debut_epargne')
    list_filter = ('periode', 'statut')
    search_fields = ('compte__numero_compte',)
    raw_id_fields = ('compte',)
    
    def get_compte(self, obj):
        return obj.compte.numero_compte
    get_compte.short_description = 'Compte'
