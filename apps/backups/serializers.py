from rest_framework import serializers

from .models import Backup


class BackupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backup
        fields = ("id", "farm", "created_by", "storage_url", "checksum", "size_bytes", "version", "encrypted", "created_at")
        read_only_fields = ("id", "created_by", "created_at")
