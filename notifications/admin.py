from django.contrib import admin
from django.utils.html import format_html
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'titre', 'get_user', 'type_action', 'get_priority',
        'get_lu_status', 'date_action', 'is_global'
    )
    list_filter = (
        'type_action', 'priority', 'lu', 'is_global', 
        'date_action', 'created_at'
    )
    search_fields = (
        'titre', 'description', 'user__nom', 
        'user__prenom', 'user__email'
    )
    raw_id_fields = ('user',)
    readonly_fields = ('date_lecture', 'created_at', 'updated_at')
    date_hierarchy = 'date_action'
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def get_user(self, obj):
        if obj.user:
            return obj.user.full_name
        elif obj.is_global:
            return format_html('<em style="color: blue;">Notification globale</em>')
        else:
            return format_html('<em style="color: gray;">Utilisateur supprimé</em>')
    get_user.short_description = 'Utilisateur'
    
    def get_priority(self, obj):
        colors = {
            'low': 'green',
            'medium': 'orange',
            'high': 'red',
            'urgent': 'darkred'
        }
        color = colors.get(obj.priority, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_priority_display()
        )
    get_priority.short_description = 'Priorité'
    
    def get_lu_status(self, obj):
        if obj.lu:
            return format_html('<span style="color: green;">✓ Lu</span>')
        else:
            return format_html('<span style="color: red; font-weight: bold;">✗ Non lu</span>')
    get_lu_status.short_description = 'Statut de lecture'
    
    def mark_as_read(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(lu=False).update(
            lu=True, 
            date_lecture=timezone.now()
        )
        self.message_user(request, f'{updated} notifications marquées comme lues.')
    mark_as_read.short_description = "Marquer comme lues"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.filter(lu=True).update(
            lu=False, 
            date_lecture=None
        )
        self.message_user(request, f'{updated} notifications marquées comme non lues.')
    mark_as_unread.short_description = "Marquer comme non lues"
