from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import Pret, Remboursement
from .serializers import PretSerializer, RemboursementSerializer

class PretViewSet(viewsets.ModelViewSet):
    queryset = Pret.objects.select_related('client__user', 'produit').all()
    serializer_class = PretSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        client_id = self.request.query_params.get('client_id')
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        
        statut = self.request.query_params.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)
        
        # Recherche par nom du client
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(client__user__nom__icontains=search) |
                Q(client__user__prenom__icontains=search) |
                Q(client__numero_client__icontains=search)
            )
        
        return queryset.order_by('-date_octroi')
    
    @action(detail=True, methods=['get'])
    def remboursements(self, request, pk=None):
        """Récupérer les remboursements d'un prêt"""
        pret = self.get_object()
        remboursements = pret.remboursements.all()
        serializer = RemboursementSerializer(remboursements, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Changer le statut d'un prêt"""
        pret = self.get_object()
        new_status = request.data.get('statut')
        if new_status not in ['en_cours', 'rembourse', 'impaye', 'suspendu']:
            return Response({'error': 'Statut invalide'}, status=status.HTTP_400_BAD_REQUEST)
        
        pret.statut = new_status
        pret.save()
        return Response({'message': f'Statut changé à {new_status}'})
    
    @action(detail=False, methods=['get'])
    def echeances(self, request):
        """Prêts arrivant à échéance"""
        dans_30_jours = timezone.now().date() + timedelta(days=30)
        
        prets = self.get_queryset().filter(
            date_fin__lte=dans_30_jours,
            statut='en_cours'
        )
        
        serializer = PretSerializer(prets, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques des prêts"""
        total_prets = Pret.objects.count()
        montant_prete = Pret.objects.aggregate(total=Sum('montant'))['total'] or 0
        montant_rembourse = Pret.objects.aggregate(total=Sum('montant_rembourse'))['total'] or 0
        
        # Stats par statut
        stats_par_statut = list(
            Pret.objects.values('statut').annotate(
                count=Count('id'),
                total_montant=Sum('montant')
            )
        )
        
        return Response({
            'total_prets': total_prets,
            'montant_total_prete': montant_prete,
            'montant_total_rembourse': montant_rembourse,
            'stats_par_statut': stats_par_statut,
        })

class RemboursementViewSet(viewsets.ModelViewSet):
    queryset = Remboursement.objects.select_related('pret__client__user').all()
    serializer_class = RemboursementSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        pret_id = self.request.query_params.get('pret_id')
        if pret_id:
            queryset = queryset.filter(pret_id=pret_id)
        
        mode_paiement = self.request.query_params.get('mode_paiement')
        if mode_paiement:
            queryset = queryset.filter(mode_paiement=mode_paiement)
        
        return queryset.order_by('-date_paiement')
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques des remboursements"""
        total_remboursements = Remboursement.objects.count()
        montant_total = Remboursement.objects.aggregate(total=Sum('montant'))['total'] or 0
        
        # Stats par mode de paiement
        stats_par_mode = list(
            Remboursement.objects.values('mode_paiement').annotate(
                count=Count('id'),
                total_montant=Sum('montant')
            )
        )
        
        return Response({
            'total_remboursements': total_remboursements,
            'montant_total': montant_total,
            'stats_par_mode': stats_par_mode,
        })
