from django.db.models import Q
from rest_framework import viewsets

from apps.farms.models import Farm

from .models import Breed, Cattle, Lot, LotMovement
from .serializers import BreedSerializer, CattleSerializer, LotMovementSerializer, LotSerializer


def accessible_farms(user):
    return Farm.objects.filter(Q(owner=user) | Q(memberships__user=user)).distinct()


class BreedViewSet(viewsets.ModelViewSet):
    queryset = Breed.objects.all().order_by("name")
    serializer_class = BreedSerializer


class LotViewSet(viewsets.ModelViewSet):
    serializer_class = LotSerializer

    def get_queryset(self):
        return Lot.objects.filter(farm__in=accessible_farms(self.request.user)).order_by("name")


class CattleViewSet(viewsets.ModelViewSet):
    serializer_class = CattleSerializer

    def get_queryset(self):
        return Cattle.objects.filter(farm__in=accessible_farms(self.request.user), deleted_at__isnull=True).order_by("ear_tag")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class LotMovementViewSet(viewsets.ModelViewSet):
    serializer_class = LotMovementSerializer

    def get_queryset(self):
        return LotMovement.objects.filter(cattle__farm__in=accessible_farms(self.request.user)).order_by("-started_at")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
