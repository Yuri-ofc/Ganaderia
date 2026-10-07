from rest_framework import serializers

from .models import Farm, FarmMembership, Invitation


class FarmSerializer(serializers.ModelSerializer):
    owner = serializers.UUIDField(read_only=True)

    class Meta:
        model = Farm
        fields = ("id", "owner", "name", "location", "created_at", "updated_at")
        read_only_fields = ("id", "owner", "created_at", "updated_at")


class FarmMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmMembership
        fields = ("id", "farm", "user", "role", "invited_by", "created_at", "updated_at")
        read_only_fields = ("id", "invited_by", "created_at", "updated_at")


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ("id", "farm", "phone_number", "role", "token", "status", "expires_at", "created_by", "created_at")
        read_only_fields = ("id", "token", "created_by", "created_at")
