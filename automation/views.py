from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Lead, SolarCalculation
from services.calculator import calculate_solar_system
import json

@csrf_exempt
def submit_lead_view(request):
    """
    Saves Lead, runs calculation, and returns success for Modal trigger.
    """
    if request.method == 'POST':
        # Handle both JSON and Form data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        name = data.get('name')
        phone = data.get('phone')
        city = data.get('city_area') or data.get('city', '')
        
        # Mapping 'monthly_bill' or 'units' to monthly_units
        bill_raw = data.get('monthly_bill') or 0
        bill = float(bill_raw)
        
        units_raw = data.get('units') or (bill / 60)
        units = int(units_raw)

        if not name or not phone:
            return JsonResponse({'success': False, 'error': 'Name and Phone are required.'})

        # Run calculation engine to get system size and cost
        calc_result = calculate_solar_system(bill if bill > 0 else units * 60)

        appliance_data_str = data.get('appliance_data', '{}')
        try:
            appliance_data = json.loads(appliance_data_str) if isinstance(appliance_data_str, str) else appliance_data_str
        except json.JSONDecodeError:
            appliance_data = {}

        # Merge top-level technical fields into appliance_data
        for field in ['fans', 'lights', 'iron', 'computers', 'motors', 'other_load_watts', 'wants_earth_bore', 'desired_backup_hours', 'property_type']:
            if field in data:
                appliance_data[field] = data.get(field)

        # Map and create Contact for the main CRM
        from core.models import Contact
        contact = Contact.objects.create(
            name=name,
            phone=phone,
            city_area=city,
            monthly_bill=bill,
            wapda_bill=request.FILES.get('wapda_bill'),
            appliance_data=appliance_data,
            fans=int(data.get('fans', 0) or 0),
            lights=int(data.get('lights', 0) or 0),
            ac=int(data.get('ac', 0) or 0),
            fridge=int(data.get('fridge', 0) or 0),
            heater=int(data.get('heater', 0) or 0),
            iron=int(data.get('iron', 0) or 0),
            computers=int(data.get('computers', 0) or 0),
            motors=int(data.get('motors', 0) or 0),
            other_load_watts=int(data.get('other_load_watts', 0) or 0),
            desired_backup_hours=float(data.get('desired_backup_hours', 0) or 0),
            wants_earth_bore=bool(data.get('wants_earth_bore', False)),
            property_type=data.get('property_type', 'home'),
            lead_status=Contact.LEAD_NEW
        )

        # Save Lead with full fields for Automation Dashboard
        lead = Lead.objects.create(
            name=name,
            phone=phone,
            city=city,
            monthly_units=units,
            system_size=float(calc_result['system_size_kw']),
            estimated_cost=float(calc_result['total_cost']),
            appliance_data=appliance_data
        )

        # Create SolarCalculation object to show in Django Admin inlines
        from automation.models import SolarCalculation
        SolarCalculation.objects.create(
            lead=lead,
            system_size_kw=calc_result['system_size_kw'],
            monthly_units=calc_result['monthly_units'],
            monthly_savings=calc_result['monthly_savings'],
            annual_savings=calc_result['annual_savings'],
            payback_years=calc_result['payback_years'],
            total_cost=calc_result['total_cost'],
            panel_count=calc_result['panel_count']
        )


        return JsonResponse({
            'success': True,
            'status': 'success',
            'message': 'Lead saved successfully',
            'lead_id': lead.id
        })

    return JsonResponse({'success': False, 'error': 'Invalid method.'})

def admin_leads(request):
    """
    Custom Admin Dashboard for Leads.
    """
    leads = Lead.objects.all().order_by('-created_at')
    return render(request, "admin/leads.html", {"leads": leads})
