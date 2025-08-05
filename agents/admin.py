from django.contrib import admin
from .models import Agent

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('get_nom', 'statut', 'created_at')
    list_filter = ('statut',)
    search_fields = ('user__nom', 'user__prenom')
    raw_id_fields = ('user',)
    
    def get_nom(self, obj):
        return obj.nom_complet
    get_nom.short_description = 'Nom complet'