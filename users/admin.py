from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'nom', 'prenom', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('email', 'nom', 'prenom')
    ordering = ('nom',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Info personnelles', {'fields': ('nom', 'prenom', 'telephone', 'adresse')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom', 'prenom', 'telephone', 'role', 'password1', 'password2'),
        }),
    )
