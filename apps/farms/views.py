from django.db.models import Q
from rest_framework import viewsets

from .models import Farm, FarmMembership, Invitation
from .serializers import FarmMembershipSerializer, FarmSerializer, InvitationSerializer


class FarmViewSet(viewsets.ModelViewSet):
    serializer_class = FarmSerializer

    def get_queryset(self):
        return Farm.objects.filter(Q(owner=self.request.user) | Q(memberships__user=self.request.user)).distinct().order_by("name")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MembershipQuerySetMixin:
    farm_field = "farm"

    def get_queryset(self):
        lookup = {f"{self.farm_field}__owner": self.request.user}
        return self.queryset.filter(**lookup).order_by("-created_at")


class MembershipViewSet(MembershipQuerySetMixin, viewsets.ModelViewSet):
    queryset = FarmMembership.objects.select_related("farm", "user", "invited_by")
    serializer_class = FarmMembershipSerializer

    def perform_create(self, serializer):
        serializer.save(invited_by=self.request.user)


class InvitationViewSet(MembershipQuerySetMixin, viewsets.ModelViewSet):
    queryset = Invitation.objects.select_related("farm", "created_by")
    serializer_class = InvitationSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
