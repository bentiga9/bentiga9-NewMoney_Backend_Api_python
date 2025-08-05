from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import Notification
from .serializers import NotificationSerializer, NotificationListSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.select_related('user').all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return NotificationListSerializer
        return NotificationSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'stats']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Si pas admin, filtrer les notifications de l'utilisateur + globales
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(user=self.request.user) | Q(is_global=True)
            )
        
        # Filtrer par utilisateur (pour les admins)
        user_id = self.request.query_params.get('user_id')
        if user_id and self.request.user.is_staff:
            queryset = queryset.filter(user_id=user_id)
        
        # Filtrer par statut de lecture
        lu = self.request.query_params.get('lu')
        if lu is not None:
            lu_bool = lu.lower() == 'true'
            queryset = queryset.filter(lu=lu_bool)
        
        # Filtrer par type d'action
        type_action = self.request.query_params.get('type_action')
        if type_action:
            queryset = queryset.filter(type_action=type_action)
        
        # Filtrer par priorité
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Recherche dans le titre et la description
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(titre__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset.order_by('-date_action')
    
    @action(detail=True, methods=['patch'])
    def mark_as_read(self, request, pk=None):
        """Marquer une notification comme lue"""
        notification = self.get_object()
        
        # Vérifier permissions
        if not request.user.is_staff and notification.user != request.user and not notification.is_global:
            return Response(
                {'error': 'Vous ne pouvez pas marquer cette notification comme lue'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        notification.mark_as_read()
        
        return Response({
            'message': 'Notification marquée comme lue',
            'notification': NotificationSerializer(notification).data
        })
    
    @action(detail=False, methods=['patch'])
    def mark_all_as_read(self, request):
        """Marquer toutes les notifications comme lues"""
        user_id = request.data.get('user_id') if request.user.is_staff else None
        
        if user_id and request.user.is_staff:
            # Admin marquant toutes les notifications d'un utilisateur spécifique
            queryset = Notification.objects.filter(
                Q(user_id=user_id) | Q(is_global=True),
                lu=False
            )
        elif request.user.is_staff and not user_id:
            # Admin marquant toutes les notifications du système
            queryset = Notification.objects.filter(lu=False)
        else:
            # Utilisateur normal marquant ses notifications
            queryset = Notification.objects.filter(
                Q(user=request.user) | Q(is_global=True),
                lu=False
            )
        
        count = queryset.count()
        now = timezone.now()
        
        queryset.update(lu=True, date_lecture=now)
        
        return Response({
            'message': f'{count} notifications marquées comme lues'
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def unread_count(self, request):
        """Nombre de notifications non lues pour l'utilisateur connecté"""
        count = Notification.objects.filter(
            Q(user=request.user) | Q(is_global=True),
            lu=False
        ).count()
        
        return Response({'unread_count': count})
    
    @action(detail=False, methods=['get'])
    def my_notifications(self, request):
        """Notifications de l'utilisateur connecté"""
        notifications = Notification.objects.filter(
            Q(user=request.user) | Q(is_global=True)
        ).order_by('-date_action')
        
        # Appliquer les filtres de la queryset de base
        notifications = self.filter_queryset(notifications)
        
        page = self.paginate_queryset(notifications)
        if page is not None:
            serializer = NotificationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = NotificationListSerializer(notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def stats(self, request):
        """Statistiques des notifications (réservé aux administrateurs)"""
        total_notifications = Notification.objects.count()
        notifications_lues = Notification.objects.filter(lu=True).count()
        notifications_non_lues = Notification.objects.filter(lu=False).count()
        notifications_globales = Notification.objects.filter(is_global=True).count()
        
        # Stats par type
        notifications_par_type = list(
            Notification.objects.values('type_action').annotate(
                count=Count('id')
            ).order_by('-count')
        )
        
        # Stats par priorité
        notifications_par_priorite = list(
            Notification.objects.values('priority').annotate(
                count=Count('id')
            ).order_by('-count')
        )
        
        return Response({
            'total_notifications': total_notifications,
            'notifications_lues': notifications_lues,
            'notifications_non_lues': notifications_non_lues,
            'notifications_globales': notifications_globales,
            'notifications_par_type': notifications_par_type,
            'notifications_par_priorite': notifications_par_priorite,
        })
    
    @action(detail=False, methods=['delete'], permission_classes=[IsAdminUser])
    def cleanup_old(self, request):
        """Nettoyer les anciennes notifications lues"""
        cutoff_date = timezone.now() - timedelta(days=30)
        
        deleted_count, _ = Notification.objects.filter(
            lu=True,
            date_lecture__lt=cutoff_date
        ).delete()
        
        return Response({
            'message': f'{deleted_count} anciennes notifications supprimées'
        })
