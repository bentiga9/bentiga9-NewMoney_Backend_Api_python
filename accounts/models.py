from django.db import models
from django.utils import timezone
from decimal import Decimal
import uuid

class Compte(models.Model):
    TYPE_COMPTE_CHOICES = [('epargne', 'Épargne'), ('courant', 'Courant')]
    STATUT_CHOICES = [('actif', 'Actif'), ('cloture', 'Clôturé'), ('suspendu', 'Suspendu')]
    
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='comptes')
    numero_compte = models.CharField(max_length=255, unique=True)
    type_compte = models.CharField(max_length=10, choices=TYPE_COMPTE_CHOICES)
    solde = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    date_ouverture = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='actif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.numero_compte:
            year = timezone.now().year
            prefix = 'EP' if self.type_compte == 'epargne' else 'CO'
            count = Compte.objects.filter(type_compte=self.type_compte, created_at__year=year).count() + 1
            self.numero_compte = f"{prefix}{year}{count:08d}"
        
        if not self.date_ouverture:
            self.date_ouverture = timezone.now().date()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.numero_compte} - {self.client.nom_complet}"

class Transaction(models.Model):
    TYPE_TRANSACTION_CHOICES = [('depot', 'Dépôt'), ('retrait', 'Retrait'), ('transfert', 'Transfert'), ('virement', 'Virement')]
    
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='transactions')
    type_transaction = models.CharField(max_length=10, choices=TYPE_TRANSACTION_CHOICES)
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    date_transaction = models.DateTimeField(default=timezone.now)
    reference = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    solde_apres = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = f"TXN{timezone.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.type_transaction} - {self.montant} - {self.compte.numero_compte}"

class Epargne(models.Model):
    PERIODE_CHOICES = [('90', '90 jours'), ('180', '180 jours'), ('360', '360 jours')]
    STATUT_CHOICES = [('en_cours', 'En cours'), ('termine', 'Terminé'), ('suspendu', 'Suspendu')]
    
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='epargnes')
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    taux_interet = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    periode = models.CharField(max_length=3, choices=PERIODE_CHOICES)
    date_epargne = models.DateField()
    montant_a_percevoir = models.DecimalField(max_digits=15, decimal_places=2)
    date_debut_epargne = models.DateField()
    date_fin_epargne = models.DateField()
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='en_cours')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Épargne {self.compte.numero_compte} - {self.montant}"
