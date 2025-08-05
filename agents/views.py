from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Agent
from .serializers import AgentSerializer

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.select_related('user').all()
    serializer_class = AgentSerializer
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
                Q(user__prenom__icontains=search)
            )
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Changer le statut d'un agent"""
        agent = self.get_object()
        new_status = request.data.get('statut')
        if new_status not in ['actif', 'inactif', 'suspendu']:
            return Response({'error': 'Statut invalide'}, status=status.HTTP_400_BAD_REQUEST)
        
        agent.statut = new_status
        agent.save()
        return Response({'message': f'Statut changé à {new_status}'})
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques des agents"""
        total = Agent.objects.count()
        actifs = Agent.objects.filter(statut='actif').count()
        
        return Response({
            'total_agents': total,
            'agents_actifs': actifs,
        })