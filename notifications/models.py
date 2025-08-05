from django.db import models
from django.conf import settings
from django.utils import timezone

class Notification(models.Model):
    TYPE_ACTION_CHOICES = [
        ('creation_compte', 'Création de compte'),
        ('depot', 'Dépôt'),
        ('retrait', 'Retrait'),
        ('pret_accorde', 'Prêt accordé'),
        ('remboursement', 'Remboursement'),
        ('echeance_proche', 'Échéance proche'),
        ('epargne_mature', 'Épargne arrivée à maturité'),
        ('alerte_securite', 'Alerte sécurité'),
        ('maintenance', 'Maintenance système'),
        ('autres', 'Autres'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Faible'),
        ('medium', 'Moyenne'),
        ('high', 'Élevée'),
        ('urgent', 'Urgent'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='notifications'
    )
    type_action = models.CharField(max_length=50, choices=TYPE_ACTION_CHOICES)
    titre = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    date_action = models.DateTimeField(default=timezone.now)
    lu = models.BooleanField(default=False)
    date_lecture = models.DateTimeField(null=True, blank=True)
    is_global = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_action']
        indexes = [
            models.Index(fields=['user', 'lu']),
            models.Index(fields=['type_action']),
            models.Index(fields=['date_action']),
        ]
    
    def __str__(self):
        user_str = self.user.full_name if self.user else "Global"
        return f"{self.titre} - {user_str}"
    
    def mark_as_read(self):
        if not self.lu:
            self.lu = True
            self.date_lecture = timezone.now()
            self.save()