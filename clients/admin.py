from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('numero_client', 'get_nom', 'statut', 'date_adhesion')
    list_filter = ('statut', 'date_adhesion')
    search_fields = ('numero_client', 'user__nom', 'user__prenom')
    raw_id_fields = ('user',)
    
    def get_nom(self, obj):
        return obj.nom_complet
    get_nom.short_description = 'Nom complet'