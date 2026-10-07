from rest_framework import serializers

from .models import AIModel, Device, Measurement, MeasurementType, MorphometricMeasurement, ScaleWeighing


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ("id", "owner", "model_name", "operating_system", "last_connected_at", "created_at", "updated_at")
        read_only_fields = ("id", "owner", "created_at", "updated_at")


class MorphometricMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = MorphometricMeasurement
        fields = ("id", "measurement", "measurement_type", "value", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = (
            "id", "cattle", "created_by", "device", "ai_model", "captured_at", "capture_mode",
            "estimated_weight_kg", "confidence_interval_min_kg", "confidence_interval_max_kg",
            "body_condition_score", "confidence_level", "corrects", "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_by", "created_at", "updated_at")

    def validate(self, attrs):
        lower = attrs.get("confidence_interval_min_kg", getattr(self.instance, "confidence_interval_min_kg", None))
        upper = attrs.get("confidence_interval_max_kg", getattr(self.instance, "confidence_interval_max_kg", None))
        if lower is not None and upper is not None and lower > upper:
            raise serializers.ValidationError({"confidence_interval_max_kg": "Debe ser mayor o igual al límite inferior."})
        return attrs


class ScaleWeighingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScaleWeighing
        fields = ("id", "cattle", "created_by", "weighed_at", "scale_type", "actual_weight_kg", "corrects", "created_at", "updated_at")
        read_only_fields = ("id", "created_by", "created_at", "updated_at")
