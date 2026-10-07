from rest_framework import serializers

from .models import SyncChange


class SyncChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyncChange
        fields = ("id", "farm", "device", "created_by", "resource", "object_id", "action", "payload", "synchronized_at", "created_at", "updated_at")
        read_only_fields = ("id", "created_by", "created_at", "updated_at")
