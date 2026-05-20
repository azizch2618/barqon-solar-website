import json
import logging
import time

from django.db import OperationalError, close_old_connections, transaction
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Lead, SolarCalculation
from services.calculator import calculate_solar_system

logger = logging.getLogger("barqon")


def _is_sqlite_lock_error(exc):
    message = str(exc).lower()
    return "database is locked" in message or "disk i/o error" in message


def _write_with_retry(callback, attempts=3):
    last_error = None
    for attempt in range(attempts):
        close_old_connections()
        try:
            with transaction.atomic():
                return callback()
        except OperationalError as exc:
            last_error = exc
            if not _is_sqlite_lock_error(exc) or attempt == attempts - 1:
                raise
            logger.warning("SQLite write contention while saving quote lead; retrying.", exc_info=True)
            time.sleep(0.25 * (attempt + 1))
        finally:
            close_old_connections()
    raise last_error

@csrf_exempt
def submit_lead_view(request):
    """
    Saves Lead, runs calculation, and returns success for Modal trigger.
    """
    if request.method == 'POST':
        def clean_number(value, default=0, cast=float):
            if value in (None, "", "null", "undefined"):
                return default
            try:
                return cast(value)
            except (TypeError, ValueError):
                return default

        def clean_bool(value):
            if isinstance(value, bool):
                return value
            return str(value).strip().lower() in {"1", "true", "yes", "on"}

        # Handle both JSON and form data while keeping failures JSON-safe.
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body or "{}")
            else:
                data = request.POST
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid request payload.'}, status=400)

        name = data.get('name')
        phone = data.get('phone')
        city = data.get('city_area') or data.get('city', '')
        
        # Mapping 'monthly_bill' or 'units' to monthly_units
        bill = clean_number(data.get('monthly_bill'), 0, float)
        
        units_raw = data.get('units')
        units = clean_number(units_raw, bill / 60 if bill else 0, int)

        if not name or not phone:
            return JsonResponse({'success': False, 'error': 'Name and Phone are required.'}, status=400)

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
        try:
            customer_message = data.get('message') or 'Solar quotation request from website.'

            def create_records():
                contact = Contact.objects.create(
                    name=name,
                    email=data.get('email', ''),
                    phone=phone,
                    subject=data.get('subject') or 'Solar Quotation Request',
                    message=customer_message,
                    city_area=city,
                    monthly_bill=bill,
                    wapda_bill=request.FILES.get('wapda_bill'),
                    appliance_data=appliance_data,
                    fans=clean_number(data.get('fans'), 0, int),
                    lights=clean_number(data.get('lights'), 0, int),
                    ac=clean_number(data.get('ac'), 0, int),
                    fridge=clean_number(data.get('fridge'), 0, int),
                    heater=clean_number(data.get('heater'), 0, int),
                    iron=clean_number(data.get('iron'), 0, int),
                    computers=clean_number(data.get('computers'), 0, int),
                    motors=clean_number(data.get('motors'), 0, int),
                    other_load_watts=clean_number(data.get('other_load_watts'), 0, int),
                    desired_backup_hours=clean_number(data.get('desired_backup_hours'), 0, float),
                    wants_earth_bore=clean_bool(data.get('wants_earth_bore')),
                    property_type=data.get('property_type') or Contact.PROPERTY_HOME,
                    system_type_preference=data.get('system_type_preference') or Contact.SYSTEM_NOT_SURE,
                    preferred_contact_method=data.get('preferred_contact_method') or Contact.CONTACT_CALL,
                    lead_status=Contact.LEAD_NEW
                )

                lead = Lead.objects.create(
                    name=name,
                    phone=phone,
                    city=city,
                    monthly_units=units,
                    system_size=float(calc_result['system_size_kw']),
                    estimated_cost=float(calc_result['total_cost']),
                    appliance_data=appliance_data
                )

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
                return contact, lead

            contact, lead = _write_with_retry(create_records)
        except OperationalError as exc:
            logger.exception("Database failure while saving public quote lead.")
            if _is_sqlite_lock_error(exc):
                return JsonResponse({
                    'success': False,
                    'error': 'The server is busy saving another request. Please try again in a few seconds.'
                }, status=503)
            return JsonResponse({
                'success': False,
                'error': 'A database error prevented saving your request. Please try again.'
            }, status=500)
        except Exception as exc:
            logger.exception("Quote lead validation/save failure.")
            return JsonResponse({
                'success': False,
                'error': 'We could not save the lead. Please review the form and try again.',
                'debug': str(exc) if request.user.is_staff else ''
            }, status=400)

        # Generate WhatsApp message securely
        import urllib.parse
        from django.utils import timezone
        from core.models import CompanyProfile

        company = CompanyProfile.objects.first()
        wa_number = company.cleaned_whatsapp if company and company.cleaned_whatsapp else "923009132042"
        
        customer_message = data.get('message', 'Solar Quotation Request')
        
        wa_text = f"*New Solar Lead Received!* 🌞\n\n*Customer Details:*\n👤 Name: {name}\n📞 Phone: {phone}\n📍 City: {city}\n⚡ System Size: {calc_result['system_size_kw']} kW\n📝 Message: {customer_message}\n⏱️ Time: {timezone.localtime(timezone.now()).strftime('%d-%b-%Y %I:%M %p')}\n\n_Please contact the customer ASAP._"
        
        wa_url = f"https://wa.me/{wa_number}?text={urllib.parse.quote(wa_text)}"

        return JsonResponse({
            'success': True,
            'status': 'success',
            'message': 'Lead saved successfully',
            'lead_id': lead.id,
            'whatsapp_url': wa_url
        })

    return JsonResponse({'success': False, 'error': 'Invalid method.'})

def admin_leads(request):
    """
    Custom Admin Dashboard for Leads.
    """
    leads = Lead.objects.all().order_by('-created_at')
    return render(request, "admin/leads.html", {"leads": leads})
