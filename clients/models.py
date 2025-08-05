from django.db import models
from django.conf import settings
from django.utils import timezone

class Client(models.Model):
    STATUT_CHOICES = [('actif', 'Actif'), ('suspendu', 'Suspendu'), ('inactif', 'Inactif')]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_profile')
    numero_client = models.CharField(max_length=255, unique=True)
    date_adhesion = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='actif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.numero_client:
            year = timezone.now().year
            count = Client.objects.filter(created_at__year=year).count() + 1
            self.numero_client = f"CL{year}{count:06d}"
        if not self.date_adhesion:
            self.date_adhesion = timezone.now().date()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.numero_client} - {self.user.full_name}"
    
    @property
    def nom_complet(self):
        return self.user.full_name