from decimal import Decimal

from rest_framework import serializers

from .models import LoadCalculation


class LoadCalculationInputSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=120, required=False, allow_blank=True)
    property_type = serializers.CharField(max_length=30, required=False, allow_blank=True)
    city_area = serializers.CharField(max_length=150, required=False, allow_blank=True)
    fans = serializers.IntegerField(min_value=0, default=0)
    lights = serializers.IntegerField(min_value=0, default=0)
    ac = serializers.IntegerField(min_value=0, default=0)
    fridge = serializers.IntegerField(min_value=0, default=0)
    heater = serializers.IntegerField(min_value=0, default=0)
    iron = serializers.IntegerField(min_value=0, default=0)
    computers = serializers.IntegerField(min_value=0, default=0)
    motors = serializers.IntegerField(min_value=0, default=0)
    other_load_watts = serializers.IntegerField(min_value=0, default=0)
    monthly_units = serializers.IntegerField(min_value=0, required=False, allow_null=True)
    monthly_bill = serializers.FloatField(min_value=0, required=False, allow_null=True)
    total_watts = serializers.IntegerField(min_value=0, required=False, allow_null=True)
    average_sun_hours = serializers.DecimalField(max_digits=4, decimal_places=2, default=Decimal("5.00"))
    backup_hours = serializers.DecimalField(max_digits=4, decimal_places=2, default=Decimal("5.00"))
    battery_voltage = serializers.IntegerField(min_value=1, default=12)
    save_result = serializers.BooleanField(default=False)


class LoadCalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadCalculation
        fields = "__all__"
        read_only_fields = ["user", "created_at"]
