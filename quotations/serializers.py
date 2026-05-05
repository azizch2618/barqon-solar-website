from rest_framework import serializers

from .models import Quotation


class QuotationSerializer(serializers.ModelSerializer):
    prepared_by_name = serializers.SerializerMethodField()

    revision_count = serializers.IntegerField(source='revisions.count', read_only=True)

    class Meta:
        model = Quotation
        fields = "__all__"
        read_only_fields = [
            "quotation_number",
            "version_number",
            "prepared_by",
            "prepared_by_name",
            "revision_count",
            "created_at",
            "updated_at",
        ]

    def get_prepared_by_name(self, obj):
        if not obj.prepared_by:
            return ""
        full_name = f"{obj.prepared_by.first_name} {obj.prepared_by.last_name}".strip()
        return full_name or obj.prepared_by.username
