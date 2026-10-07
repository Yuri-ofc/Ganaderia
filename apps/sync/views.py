from rest_framework import viewsets

from apps.cattle.views import accessible_farms

from .models import SyncChange
from .serializers import SyncChangeSerializer


class SyncChangeViewSet(viewsets.ModelViewSet):
    serializer_class = SyncChangeSerializer

    def get_queryset(self):
        return SyncChange.objects.filter(farm__in=accessible_farms(self.request.user)).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
