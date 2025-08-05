from django.contrib import admin
from .models import Condition, Produit

@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = ('nom', 'created_at')
    search_fields = ('nom',)

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'taux_interet', 'is_active')
    list_filter = ('type', 'is_active')
    search_fields = ('nom',)