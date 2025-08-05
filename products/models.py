from django.db import models
from decimal import Decimal

class Condition(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nom

class Produit(models.Model):
    TYPE_CHOICES = [('commerce', 'Commerce'), ('scolaire', 'Scolaire'), ('immobilier', 'Immobilier')]
    DUREE_CHOICES = [('6', '6 mois'), ('12', '12 mois'), ('24', '24 mois')]
    
    nom = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    taux_interet = models.DecimalField(max_digits=5, decimal_places=2)
    frais = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('5000.00'))
    duree = models.CharField(max_length=2, choices=DUREE_CHOICES)
    conditions = models.ForeignKey(Condition, on_delete=models.CASCADE, related_name='produits')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nom} - {self.get_type_display()}"