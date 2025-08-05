from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from .models import Compte, Transaction, Epargne
from .serializers import CompteSerializer, TransactionSerializer, EpargneSerializer

class CompteViewSet(viewsets.ModelViewSet):
    queryset = Compte.objects.select_related('client__user').all()
    serializer_class = CompteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        client_id = self.request.query_params.get('client_id')
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        
        type_compte = self.request.query_params.get('type_compte')
        if type_compte:
            queryset = queryset.filter(type_compte=type_compte)
        
        statut = self.request.query_params.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)
        
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        """Récupérer les transactions d'un compte"""
        compte = self.get_object()
        transactions = compte.transactions.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques des comptes"""
        total_comptes = Compte.objects.count()
        comptes_actifs = Compte.objects.filter(statut='actif').count()
        solde_total = Compte.objects.aggregate(total=Sum('solde'))['total'] or 0
        
        return Response({
            'total_comptes': total_comptes,
            'comptes_actifs': comptes_actifs,
            'solde_total': solde_total,
        })

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.select_related('compte__client__user').all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        compte_id = self.request.query_params.get('compte_id')
        if compte_id:
            queryset = queryset.filter(compte_id=compte_id)
        
        type_transaction = self.request.query_params.get('type_transaction')
        if type_transaction:
            queryset = queryset.filter(type_transaction=type_transaction)
        
        return queryset.order_by('-date_transaction')
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques des transactions"""
        total = Transaction.objects.count()
        montant_total = Transaction.objects.aggregate(total=Sum('montant'))['total'] or 0
        
        # Stats par type
        stats_par_type = list(
            Transaction.objects.values('type_transaction').annotate(
                count=Count('id'),
                total_montant=Sum('montant')
            )
        )
        
        return Response({
            'total_transactions': total,
            'montant_total': montant_total,
            'stats_par_type': stats_par_type,
        })

class EpargneViewSet(viewsets.ModelViewSet):
    queryset = Epargne.objects.select_related('compte__client__user').all()
    serializer_class = EpargneSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        compte_id = self.request.query_params.get('compte_id')
        if compte_id:
            queryset = queryset.filter(compte_id=compte_id)
        
        statut = self.request.query_params.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)
        
        return queryset.order_by('-date_debut_epargne')
