from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import Client
from .serializers import ClientSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.select_related('user').all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        statut = self.request.query_params.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)
        
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(user__nom__icontains=search) |
                Q(user__prenom__icontains=search) |
                Q(numero_client__icontains=search)
            )
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Changer le statut d'un client"""
        client = self.get_object()
        new_status = request.data.get('statut')
        if new_status not in ['actif', 'suspendu', 'inactif']:
            return Response({'error': 'Statut invalide'}, status=status.HTTP_400_BAD_REQUEST)
        
        client.statut = new_status
        client.save()
        return Response({'message': f'Statut changé à {new_status}'})
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques des clients"""
        total = Client.objects.count()
        actifs = Client.objects.filter(statut='actif').count()
        suspendus = Client.objects.filter(statut='suspendu').count()
        
        debut_mois = timezone.now().replace(day=1)
        nouveaux_mois = Client.objects.filter(created_at__gte=debut_mois).count()
        
        return Response({
            'total_clients': total,
            'clients_actifs': actifs,
            'clients_suspendus': suspendus,
            'nouveaux_clients_mois': nouveaux_mois,
        })
