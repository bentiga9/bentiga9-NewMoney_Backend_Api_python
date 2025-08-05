from django.db import models
from django.utils import timezone
from decimal import Decimal

class Pret(models.Model):
    STATUT_CHOICES = [('en_cours', 'En cours'), ('rembourse', 'Remboursé'), ('impaye', 'Impayé'), ('suspendu', 'Suspendu')]
    
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='prets')
    produit = models.ForeignKey('products.Produit', on_delete=models.SET_NULL, null=True, blank=True, related_name='prets')
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    taux_interet = models.DecimalField(max_digits=5, decimal_places=2)
    duree = models.IntegerField()  # en mois
    date_octroi = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    montant_total_a_rembourser = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    montant_rembourse = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default='en_cours')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Calculer le montant total à rembourser
        if not self.montant_total_a_rembourser:
            interet = (self.montant * self.taux_interet * self.duree) / (100 * 12)
            self.montant_total_a_rembourser = self.montant + interet
        
        # Calculer la date de fin si non fournie
        if not self.date_fin and self.date_octroi:
            from dateutil.relativedelta import relativedelta
            self.date_fin = self.date_octroi + relativedelta(months=self.duree)
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Prêt {self.client.nom_complet} - {self.montant}"
    
    @property
    def montant_restant(self):
        return self.montant_total_a_rembourser - self.montant_rembourse

class Remboursement(models.Model):
    MODE_PAIEMENT_CHOICES = [('cash', 'Cash'), ('mobile_money', 'Mobile Money'), ('virement', 'Virement'), ('cheque', 'Chèque')]
    
    pret = models.ForeignKey(Pret, on_delete=models.CASCADE, related_name='remboursements')
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    date_paiement = models.DateField()
    mode_paiement = models.CharField(max_length=15, choices=MODE_PAIEMENT_CHOICES)
    reference = models.CharField(max_length=255, null=True, blank=True)
    justificatif_url = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.reference:
            import uuid
            self.reference = f"REM{timezone.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4())[:6].upper()}"
        
        super().save(*args, **kwargs)
        
        # Mettre à jour le montant remboursé du prêt
        self.pret.montant_rembourse = self.pret.remboursements.aggregate(
            total=models.Sum('montant')
        )['total'] or Decimal('0.00')
        
        # Mettre à jour le statut du prêt si entièrement remboursé
        if self.pret.montant_rembourse >= self.pret.montant_total_a_rembourser:
            self.pret.statut = 'rembourse'
        
        self.pret.save()
    
    def __str__(self):
        return f"Remboursement {self.pret.client.nom_complet} - {self.montant}"

