from rest_framework import serializers

from .models import Breed, Cattle, Lot, LotMovement


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ("id", "name", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class LotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lot
        fields = ("id", "farm", "name", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class CattleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cattle
        fields = (
            "id", "farm", "lot", "ear_tag", "breed", "sex", "productive_category",
            "physiological_status", "estimated_birth_date", "operational_status", "profile_photo_url",
            "profile_approved_by", "created_by", "deactivated_at", "deactivation_reason", "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_by", "created_at", "updated_at")

    def validate(self, attrs):
        farm = attrs.get("farm", getattr(self.instance, "farm", None))
        lot = attrs.get("lot", getattr(self.instance, "lot", None))
        if farm and lot and lot.farm_id != farm.id:
            raise serializers.ValidationError({"lot": "El lote debe pertenecer a la misma finca."})
        return attrs


class LotMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = LotMovement
        fields = ("id", "cattle", "lot", "started_at", "ended_at", "created_by", "created_at", "updated_at")
        read_only_fields = ("id", "created_by", "created_at", "updated_at")

    def validate(self, attrs):
        cattle = attrs.get("cattle", getattr(self.instance, "cattle", None))
        lot = attrs.get("lot", getattr(self.instance, "lot", None))
        if cattle and lot and cattle.farm_id != lot.farm_id:
            raise serializers.ValidationError({"lot": "El lote debe pertenecer a la finca del bovino."})
        return attrs
