from django.db import models
from django.conf import settings

class Agent(models.Model):
    STATUT_CHOICES = [('actif', 'Actif'), ('inactif', 'Inactif'), ('suspendu', 'Suspendu')]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agent_profile')
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='actif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Agent {self.user.full_name}"
    
    @property
    def nom_complet(self):
        return self.user.full_name