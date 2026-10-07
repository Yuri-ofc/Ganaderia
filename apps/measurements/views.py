from rest_framework import viewsets

from apps.cattle.views import accessible_farms

from .models import Device, Measurement, ScaleWeighing
from .serializers import DeviceSerializer, MeasurementSerializer, ScaleWeighingSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user).order_by("-last_connected_at")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MeasurementViewSet(viewsets.ModelViewSet):
    serializer_class = MeasurementSerializer
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        return Measurement.objects.filter(cattle__farm__in=accessible_farms(self.request.user)).order_by("-captured_at")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ScaleWeighingViewSet(viewsets.ModelViewSet):
    serializer_class = ScaleWeighingSerializer
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        return ScaleWeighing.objects.filter(cattle__farm__in=accessible_farms(self.request.user)).order_by("-weighed_at")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
