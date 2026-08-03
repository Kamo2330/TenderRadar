from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import AlertPreference, Source, Tender

User = get_user_model()


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ("id", "name", "slug")


class TenderSerializer(serializers.ModelSerializer):
    source = SourceSerializer(read_only=True)
    download_url = serializers.CharField(read_only=True)

    class Meta:
        model = Tender
        fields = (
            "id",
            "external_id",
            "title",
            "description",
            "department",
            "category",
            "tender_type",
            "province",
            "published_date",
            "closing_date",
            "url",
            "download_url",
            "source",
            "created_at",
        )


class AlertPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertPreference
        fields = (
            "keywords",
            "departments",
            "provinces",
            "delivery_email",
            "delivery_telegram",
            "delivery_whatsapp",
            "frequency",
        )


class UserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(read_only=True)
    is_client = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "email", "is_staff", "is_client")

    def get_is_client(self, obj) -> bool:
        return hasattr(obj, "client_profile")


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
