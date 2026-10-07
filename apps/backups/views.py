from rest_framework import viewsets

from apps.cattle.views import accessible_farms

from .models import Backup
from .serializers import BackupSerializer


class BackupViewSet(viewsets.ModelViewSet):
    serializer_class = BackupSerializer

    def get_queryset(self):
        return Backup.objects.filter(farm__in=accessible_farms(self.request.user)).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
