from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.permissions import IsOwnerOrAdmin

from .models import LoadCalculation
from .serializers import LoadCalculationInputSerializer, LoadCalculationSerializer
from .services import build_load_summary


@api_view(["POST"])
@permission_classes([AllowAny])
def calculate_load(request):
    serializer = LoadCalculationInputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    payload = serializer.validated_data
    
    # NEW LOGIC: support both monthly_bill and total_watts
    monthly_bill = payload.get("monthly_bill")
    total_watts = payload.get("total_watts")
    
    if (monthly_bill is not None and monthly_bill > 0) or (total_watts is not None and total_watts > 0):
        import math
        import random
        
        tariff = 50.0  # assumed tariff
        
        if monthly_bill and monthly_bill > 0:
            units = float(monthly_bill) / tariff
            daily_units = units / 30.0
            kw = daily_units / 5.5
            monthly_savings = float(monthly_bill) * 0.7
        else:
            kw = float(total_watts) / 1000.0
            daily_units = kw * 5.5
            units = daily_units * 30.0
            monthly_bill = units * tariff
            monthly_savings = float(monthly_bill) * 0.7

        panels = (kw * 1000) / 550.0
        cost = kw * 250000.0
        roi_years = cost / (monthly_savings * 12) if monthly_savings > 0 else 0
        
        savings_data = [{"month": m, "savings": round(monthly_savings)} for m in ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']]
        production_data = [{"month": m, "kwh": round(kw * 5.5 * 30 * (1 + (random.random()*0.1 - 0.05)))} for m in ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']]
        
        response_data = {
            "kw": round(kw, 2),
            "panels": math.ceil(panels),
            "cost": round(cost, 2),
            "monthlySavings": round(monthly_savings, 2),
            "roiYears": round(roi_years, 1),
            "savingsData": savings_data,
            "productionData": production_data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    summary = build_load_summary(payload)

    saved_record = None
    should_save = payload.get("save_result", False)
    is_owner = (
        request.user.is_authenticated
        and (
            request.user.is_staff
            or request.user.is_superuser
            or getattr(request.user, "is_admin", False)
        )
    )

    if should_save and is_owner:
        saved_record = LoadCalculation.objects.create(
            user=request.user,
            customer_name=payload.get("customer_name", ""),
            property_type=payload.get("property_type", ""),
            city_area=payload.get("city_area", ""),
            fans=payload["fans"],
            lights=payload["lights"],
            ac=payload["ac"],
            fridge=payload["fridge"],
            heater=payload["heater"],
            iron=payload["iron"],
            computers=payload["computers"],
            motors=payload["motors"],
            other_load_watts=payload["other_load_watts"],
            average_sun_hours=payload["average_sun_hours"],
            backup_hours=payload["backup_hours"],
            battery_voltage=payload["battery_voltage"],
            **summary,
        )

    response_data = {
        **summary,
        "recommended_panel_capacity_kw": str(summary["solar_required_kw"]),
        "recommended_inverter_size_kw": str(summary["inverter_required_kw"]),
        "recommended_battery_size_kwh": str(summary["battery_required_kwh"]),
    }
    if saved_record:
        response_data["saved_calculation"] = LoadCalculationSerializer(saved_record).data

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsOwnerOrAdmin])
def calculation_history(request):
    queryset = LoadCalculation.objects.all()
    serializer = LoadCalculationSerializer(queryset, many=True)
    return Response(serializer.data)
