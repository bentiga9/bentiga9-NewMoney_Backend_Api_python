from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count
from .models import Condition, Produit
from .serializers import ConditionSerializer, ProduitSerializer

class ConditionViewSet(viewsets.ModelViewSet):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
    permission_classes = [IsAuthenticated]

class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.select_related('conditions').all()
    serializer_class = ProduitSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        type_produit = self.request.query_params.get('type')
        if type_produit:
            queryset = queryset.filter(type=type_produit)
        
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(nom__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset.order_by('nom')
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """Activer/désactiver un produit"""
        produit = self.get_object()
        produit.is_active = not produit.is_active
        produit.save()
        
        status_text = "activé" if produit.is_active else "désactivé"
        return Response({'message': f'Produit {status_text}'})
    
    @action(detail=False, methods=['get'])
    def active_only(self, request):
        """Retourner seulement les produits actifs"""
        produits_actifs = self.get_queryset().filter(is_active=True)
        serializer = ProduitSerializer(produits_actifs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques des produits"""
        total = Produit.objects.count()
        actifs = Produit.objects.filter(is_active=True).count()
        
        # Stats par type
        stats_par_type = list(
            Produit.objects.values('type').annotate(count=Count('id'))
        )
        
        return Response({
            'total_produits': total,
            'produits_actifs': actifs,
            'stats_par_type': stats_par_type,
        })
