from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.crypto import get_random_string
from rest_framework import status, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from blog.models import Post
from calculator.models import LoadCalculation
from calculator.services import build_load_summary
from quotations.models import Quotation
from quotations.views import build_quotation_pdf_response, user_can_access_quotation, render_quotation_view

from .forms import (
    CustomerProfileForm,
    PublicSolarInquiryForm,
    UnifiedLoginForm,
    UnifiedRegistrationForm,
)
from .models import (
    CompanyProfile, Contact, Project, StaffProfile, Payroll,
    SiteReview, InstallationProject, ProjectFinancials, JobPosition, JobApplication
)
from .permissions import IsOwnerOrAdmin
from .serializers import (
    CompanyProfileSerializer, 
    ContactSerializer, 
    ProjectSerializer, 
    StaffProfileSerializer,
    PayrollSerializer,
    SiteReviewSerializer,
    InstallationProjectSerializer,
    ProjectFinancialsSerializer,
    JobPositionSerializer,
    JobApplicationSerializer
)


class SiteReviewViewSet(viewsets.ModelViewSet):
    queryset = SiteReview.objects.all()
    serializer_class = SiteReviewSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        if self.action in ['list', 'retrieve']:
            # If requesting from a context that needs unapproved reviews, check auth
            if is_owner_user(self.request.user):
                return [permissions.IsAuthenticated()]
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        if is_owner_user(self.request.user):
            return qs
        return qs.filter(is_approved=True)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def approve(self, request, pk=None):
        review = self.get_object()
        review.is_approved = True
        review.save()
        return Response({'status': 'approved'})


class InstallationProjectViewSet(viewsets.ModelViewSet):
    queryset = InstallationProject.objects.all()
    serializer_class = InstallationProjectSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        featured = self.request.query_params.get('featured')
        if featured:
            qs = qs.filter(is_featured=True)
        return qs


def is_owner_user(user):
    return bool(
        user.is_authenticated
        and (user.is_staff or user.is_superuser or getattr(user, "is_admin", False))
    )





def _get_company_profile():
    return CompanyProfile.objects.first()


def _quote_queryset_for_user(user):
    if is_owner_user(user):
        return Quotation.objects.all()
    if not user.is_authenticated:
        return Quotation.objects.none()

    email_query = Q()
    if user.email:
        email_query = Q(customer_email__iexact=user.email)

    return Quotation.objects.filter(
        Q(customer_user=user) | email_query | Q(lead__linked_user=user)
    ).distinct()


def _lead_queryset_for_user(user):
    if is_owner_user(user):
        return Contact.objects.all()
    if not user.is_authenticated:
        return Contact.objects.none()

    email_query = Q()
    if user.email:
        email_query = Q(email__iexact=user.email)

    return Contact.objects.filter(Q(linked_user=user) | email_query).distinct()


def _sync_user_records(user):
    if not user.is_authenticated or not user.email:
        return

    Contact.objects.filter(linked_user__isnull=True, email__iexact=user.email).update(
        linked_user=user
    )
    Quotation.objects.filter(customer_user__isnull=True, customer_email__iexact=user.email).update(
        customer_user=user
    )


def _build_summary_from_contact(contact):
    return build_load_summary(
        {
            "property_type": contact.property_type,
            "fans": contact.fans,
            "lights": contact.lights,
            "ac": contact.ac,
            "fridge": contact.fridge,
            "heater": contact.heater,
            "iron": contact.iron,
            "computers": contact.computers,
            "motors": contact.motors,
            "other_load_watts": contact.other_load_watts,
            "average_sun_hours": Decimal("5.00"),
            "backup_hours": contact.desired_backup_hours or Decimal("0.00"),
            "battery_voltage": 48,
        }
    )


def _prefill_quotation_from_lead(lead):
    summary = _build_summary_from_contact(lead)
    customer_user = lead.linked_user

    return {
        "lead": lead,
        "customer_user": customer_user,
        "customer_name": lead.name,
        "customer_email": lead.email,
        "customer_phone": lead.phone,
        "address": lead.installation_address or lead.city_area,
        "project_title": f"{lead.get_property_type_display()} Solar Proposal",
        "system_size": summary["solar_required_kw"],
        "panel_capacity_kw": summary["solar_required_kw"],
        "panel_wattage": 585,
        "panel_count": max(1, int((summary["solar_required_kw"] * 1000) / Decimal("585"))),
        "panel_brand": "Longi / Jinko / Canadian Solar",
        "inverter": "Hybrid Solar Inverter",
        "inverter_brand": "Inverex / Solis / Growatt",
        "inverter_size_kw": summary["inverter_required_kw"],
        "battery": "Battery Backup Bank",
        "battery_type": (
            Quotation.BATTERY_LEAD_ACID
            if lead.battery_preference == Contact.BATTERY_LEAD_ACID
            else Quotation.BATTERY_LITHIUM
        ),
        "battery_brand": "Narada / Pylontech / Osaka / Phoenix",
        "battery_size_kwh": summary["battery_required_kwh"],
        "battery_backup_hours": lead.desired_backup_hours,
        "breaker_count": 4,
        "spd_count": 2,
        "dc_wire_length_m": Decimal("90.00"),
        "dc_wire_size_mm": "6 mm",
        "ac_wire_length_m": Decimal("65.00"),
        "ac_wire_size_mm": "10 mm",
        "earth_bore_included": lead.wants_earth_bore,
        "delivery_timeline": "5 to 7 working days after approval",
        "payment_terms": "50% advance, 40% before installation, 10% after commissioning.",
        "warranty_terms": "Panels as per manufacturer warranty. Inverter and battery warranty as per selected brand.",
        "client_request_summary": (
            f"Property type: {lead.get_property_type_display()}\n"
            f"Area: {lead.city_area or 'Not shared'}\n"
            f"Preferred system: {lead.get_system_type_preference_display()}\n"
            f"Battery preference: {lead.get_battery_preference_display()}\n"
            f"Backup required: {lead.desired_backup_hours} hours\n"
            f"Customer note: {lead.message}"
        ),
        "recommended_brands": (
            "Panels: Longi, Jinko, Canadian Solar\n"
            "Inverter: Inverex, Solis, Growatt\n"
            "Battery: Narada, Pylontech, Osaka, Phoenix"
        ),
        "notes": "Site survey, mounting layout, protection sizing, and final cable route will be confirmed before installation.",
    }, summary


@api_view(["GET"])
@permission_classes([AllowAny])
def api_home(request):
    return Response(
        {
            "message": "BARQON Solar API is running.",
            "modules": [
                "authentication",
                "company profile",
                "quotations",
                "blog",
                "contact leads",
                "load calculator",
            ],
        }
    )


def home(request):
    profile = _get_company_profile()
    featured_posts = Post.objects.filter(is_published=True)[:6]
    inquiry_form = PublicSolarInquiryForm()
    calculation_result = None
    submitted_lead = None

    if request.method == "POST":
        inquiry_form = PublicSolarInquiryForm(request.POST, request.FILES)
        if inquiry_form.is_valid():
            lead = inquiry_form.save(commit=False)
            if request.user.is_authenticated and not is_owner_user(request.user):
                lead.linked_user = request.user
            lead.save()
            calculation_result = _build_summary_from_contact(lead)
            submitted_lead = lead
            LoadCalculation.objects.create(
                user=request.user if request.user.is_authenticated else None,
                customer_name=lead.name,
                property_type=lead.property_type,
                city_area=lead.city_area,
                fans=lead.fans,
                lights=lead.lights,
                ac=lead.ac,
                fridge=lead.fridge,
                heater=lead.heater,
                iron=lead.iron,
                computers=lead.computers,
                motors=lead.motors,
                other_load_watts=lead.other_load_watts,
                average_sun_hours=Decimal("5.00"),
                backup_hours=lead.desired_backup_hours,
                battery_voltage=48,
                **calculation_result,
            )
            messages.success(
                request,
                "Our engineer will contact you.",
            )
            return redirect("/#quote?success=true")

    # Only show most recent 3 reviews on homepage
    site_reviews = SiteReview.objects.filter(is_approved=True)[:3]
    # Only show most recent 4 projects on homepage
    installation_projects = InstallationProject.objects.all().prefetch_related('photos')[:4]

    return render(
        request,
        "home.html",
        {
            "company": profile,
            "featured_posts": featured_posts,
            "inquiry_form": inquiry_form,
            "calculation_result": calculation_result,
            "submitted_lead": submitted_lead,
            "site_reviews": site_reviews,
            "installation_projects": installation_projects,
        },
    )


def projects_gallery_view(request):
    profile = CompanyProfile.objects.first()
    projects = InstallationProject.objects.all().prefetch_related('photos')
    return render(request, "projects_gallery.html", {
        "company": profile,
        "projects": projects,
    })


def reviews_gallery_view(request):
    profile = CompanyProfile.objects.first()
    reviews = SiteReview.objects.filter(is_approved=True).prefetch_related('photos')
    return render(request, "reviews_gallery.html", {
        "company": profile,
        "reviews": reviews,
    })


def unified_login_view(request):
    # If user is already authenticated, we still show the login page 
    # but with context that they are already logged in.
    # This allows "Always ask for login" behavior.
    is_already_logged_in = request.user.is_authenticated

    form = UnifiedLoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        if is_owner_user(user):
            return redirect("admin_dashboard")
        return redirect("customer-dashboard")

    return render(request, "auth/login.html", {
        "form": form, 
        "company": _get_company_profile(),
        "is_already_logged_in": is_already_logged_in
    })


def unified_register_view(request):
    # We no longer automatically redirect authenticated users.
    # This prevents the "Join" link from being a secret shortcut to the admin panel.
    is_already_logged_in = request.user.is_authenticated

    form = UnifiedRegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        _sync_user_records(user)
        login(request, user)
        messages.success(
            request,
            "Welcome to BARQON! Your customer portal is ready.",
        )
        return redirect("customer-dashboard")

    return render(request, "auth/register.html", {
        "form": form, 
        "company": _get_company_profile(),
        "is_already_logged_in": is_already_logged_in
    })


def customer_logout_page(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")


@login_required(login_url="/login/")
def customer_dashboard(request):
    if is_owner_user(request.user):
        return redirect("admin_dashboard")

    _sync_user_records(request.user)
    profile_form = CustomerProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and profile_form.is_valid():
        profile_form.save()
        _sync_user_records(request.user)
        messages.success(request, "Your profile has been updated.")
        return redirect("customer-dashboard")

    leads = _lead_queryset_for_user(request.user)
    quotations = _quote_queryset_for_user(request.user)
    latest_quote = quotations.first()

    return render(
        request,
        "portal/dashboard.html",
        {
            "company": _get_company_profile(),
            "profile_form": profile_form,
            "customer_leads": leads[:6],
            "customer_quotations": quotations[:12],
            "quotation_count": quotations.count(),
            "lead_count": leads.count(),
            "latest_quote": latest_quote,
        },
    )


@login_required(login_url="/portal/login/")
def quotation_pdf_download_page(request, id):
    quotation = get_object_or_404(Quotation.objects.select_related("customer_user", "lead"), id=id)
    if not user_can_access_quotation(request.user, quotation):
        messages.error(request, "You do not have permission to open this quotation.")
        return redirect("customer-dashboard" if request.user.is_authenticated else "customer-login")
    return build_quotation_pdf_response(request, quotation)


@login_required(login_url="/login/")
def quotation_view_page(request, id):
    return render_quotation_view(request, id)



def blog_list_page(request):
    profile = _get_company_profile()
    posts = Post.objects.filter(is_published=True)
    return render(
        request,
        "blog/list.html",
        {
            "company": profile,
            "posts": posts,
        },
    )


def blog_detail_page(request, slug):
    profile = _get_company_profile()
    post = get_object_or_404(Post.objects.filter(is_published=True), slug=slug)
    related_posts = Post.objects.filter(is_published=True).exclude(pk=post.pk)[:3]
    return render(
        request,
        "blog/detail.html",
        {
            "company": profile,
            "post": post,
            "related_posts": related_posts,
        },
    )


def about_us_view(request):
    profile = _get_company_profile()
    return render(request, "about.html", {"company": profile})


def careers_view(request):
    profile = _get_company_profile()
    positions = JobPosition.objects.filter(is_active=True)
    return render(request, "careers/list.html", {
        "company": profile,
        "positions": positions
    })


def job_apply_view(request, position_id):
    profile = _get_company_profile()
    position = get_object_or_404(JobPosition, id=position_id, is_active=True)
    
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        experience = request.POST.get("experience_years")
        cover_letter = request.POST.get("cover_letter")
        cv = request.FILES.get("cv")
        
        if not cv:
            messages.error(request, "Please upload your CV.")
        else:
            JobApplication.objects.create(
                position=position,
                full_name=full_name,
                email=email,
                phone=phone,
                experience_years=experience or 0,
                cover_letter=cover_letter,
                cv=cv
            )
            messages.success(request, f"Your application for {position.title} has been submitted successfully!")
            return redirect("careers-page")
            
    return render(request, "careers/apply.html", {
        "company": profile,
        "position": position
    })


def general_apply_view(request):
    profile = _get_company_profile()
    
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        experience = request.POST.get("experience_years")
        cover_letter = request.POST.get("cover_letter")
        cv = request.FILES.get("cv")
        
        if not cv:
            messages.error(request, "Please upload your CV.")
        else:
            JobApplication.objects.create(
                position=None,
                full_name=full_name,
                email=email,
                phone=phone,
                experience_years=experience or 0,
                cover_letter=cover_letter,
                cv=cv
            )
            messages.success(request, "Your general application has been submitted successfully! We will contact you if a suitable position opens up.")
            return redirect("careers-page")
            
    return render(request, "careers/apply.html", {
        "company": profile,
        "position": None
    })


# --- REST ViewSets ---





@api_view(["GET"])
@permission_classes([IsOwnerOrAdmin])
def dashboard_summary(request):
    quotations_by_status = {
        item["status"]: item["total"]
        for item in Quotation.objects.values("status").annotate(total=Count("id"))
    }

    revenue_estimate = Quotation.objects.filter(
        status__in=[Quotation.STATUS_APPROVED, Quotation.STATUS_SENT]
    ).aggregate(total_revenue=Sum("total_cost"))["total_revenue"] or Decimal("0.00")

    total_leads = Contact.objects.count()
    won_leads = Contact.objects.filter(lead_status__in=[Contact.LEAD_WON, Contact.LEAD_CLOSED]).count()
    conversion_rate = round((won_leads / total_leads * 100)) if total_leads > 0 else 0

    monthly_leads = (
        Contact.objects.annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )
    monthly_sales = (
        Quotation.objects.filter(status__in=[Quotation.STATUS_APPROVED, Quotation.STATUS_SENT])
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(revenue=Sum('total_cost'))
        .order_by('month')
    )
    monthly_expenses = (
        Payroll.objects.filter(status=Payroll.STATUS_PAID)
        .annotate(month=TruncMonth('month_year'))
        .values('month')
        .annotate(expenses=Sum('total_amount'))
        .order_by('month')
    )
    sales_dict = {item['month'].strftime("%b %Y"): float(item['revenue'] or 0) for item in monthly_sales if item['month']}
    expense_dict = {item['month'].strftime("%b %Y"): float(item['expenses'] or 0) for item in monthly_expenses if item['month']}
    chart_data = [
        {
            "month": item['month'].strftime("%b %Y"),
            "leads": item['total'],
            "revenue": sales_dict.get(item['month'].strftime("%b %Y"), 0),
            "expenses": expense_dict.get(item['month'].strftime("%b %Y"), 0),
        }
        for item in monthly_leads if item['month']
    ]

    # Lead status breakdown
    lead_status_breakdown = {
        item["lead_status"]: item["total"]
        for item in Contact.objects.values("lead_status").annotate(total=Count("id"))
    }

    # Projects breakdown
    projects_by_status = {
        item["status"]: item["total"]
        for item in Project.objects.values("status").annotate(total=Count("id"))
    }

    # Payroll totals
    total_payroll_paid = Payroll.objects.filter(status=Payroll.STATUS_PAID).aggregate(
        total=Sum('total_amount'))['total'] or Decimal("0.00")
    total_payroll_pending = Payroll.objects.filter(status=Payroll.STATUS_PENDING).aggregate(
        total=Sum('total_amount'))['total'] or Decimal("0.00")

    # Recent leads (last 5)
    recent_leads = list(Contact.objects.order_by('-created_at')[:5].values(
        'id', 'name', 'phone', 'city_area', 'lead_status', 'created_at', 'monthly_bill'
    ))

    return Response(
        {
            "company_name": CompanyProfile.objects.first().company_name
            if CompanyProfile.objects.exists()
            else "BARQON Solar Solutions",
            "quotation_count": Quotation.objects.count(),
            "blog_post_count": Post.objects.count(),
            "published_blog_count": Post.objects.filter(is_published=True).count(),
            "contact_lead_count": total_leads,
            "load_calculation_count": LoadCalculation.objects.count(),
            "quotation_status_breakdown": quotations_by_status,
            "lead_status_breakdown": lead_status_breakdown,
            "revenue_estimate": revenue_estimate,
            "closed_leads_count": won_leads,
            "conversion_rate": conversion_rate,
            "monthly_leads_chart": chart_data,
            "active_projects_count": Project.objects.filter(status__in=[Project.STATUS_PENDING, Project.STATUS_IN_PROGRESS]).count(),
            "total_projects": Project.objects.count(),
            "projects_by_status": projects_by_status,
            "staff_count": StaffProfile.objects.filter(is_active=True).count(),
            "new_lead_count": Contact.objects.filter(lead_status=Contact.LEAD_NEW).count(),
            "total_payroll_paid": total_payroll_paid,
            "total_payroll_pending": total_payroll_pending,
            "recent_leads": recent_leads,
            "total_project_cost": float(ProjectFinancials.objects.aggregate(total=Sum('total_cost'))['total'] or 0),
            "total_project_revenue": float(ProjectFinancials.objects.aggregate(total=Sum('total_revenue'))['total'] or 0),
            "total_project_profit": float(ProjectFinancials.objects.aggregate(total=Sum('profit_loss'))['total'] or 0),
            "net_profit": float(revenue_estimate) - float(total_payroll_paid),
        }
    )



class CompanyProfileViewSet(viewsets.ModelViewSet):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer
    permission_classes = [IsOwnerOrAdmin]

class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        return _lead_queryset_for_user(self.request.user)

    def perform_create(self, serializer):
        data = self.request.data
        linked_user = self.request.user if self.request.user.is_authenticated and not is_owner_user(self.request.user) else None
        lead = serializer.save(linked_user=linked_user)
        
        # Robust appliance_data parsing
        import json
        app_data = lead.appliance_data
        if isinstance(app_data, str):
            try:
                app_data = json.loads(app_data)
            except:
                app_data = {}
        
        # Complex calculation logic moved from old FBV
        total = (lead.fans * 80) + (lead.lights * 15) + (lead.fridge * 300) + (lead.iron * 1000) + (lead.computers * 100) + (lead.other_load_watts or 0)
        if lead.motors == 1: total += 750
        elif lead.motors == 2: total += 1500

        if isinstance(app_data, dict):
            acs = app_data.get('acs', [])
            if isinstance(acs, list):
                for ac_item in acs:
                    try:
                        ton = float(ac_item.get('ton', 0))
                    except (ValueError, TypeError):
                        ton = 0
                    if ton > 0:
                        total += (1200 if ton == 1 else 1800 if ton == 1.5 else 2400 if ton == 2 else 3500)
            
            def safe_int(val):
                try: return int(val)
                except: return 0

            wash_qty = safe_int(app_data.get('washing_machine', 0))
            total += (wash_qty * 500)
            deep_qty = safe_int(app_data.get('deep_freezer', 0))
            total += (deep_qty * 400)

            lead.load_details = (
                f"Detailed Engineering Lead.\n"
                f"Fans: {lead.fans}, Lights: {lead.lights}, ACs: {len(acs)}, Iron: {lead.iron}, "
                f"Laptops: {lead.computers}, Washing Machine: {wash_qty}, Freezer: {deep_qty}\n"
                f"Roof: {app_data.get('roof_type', 'N/A')}, Phase: {app_data.get('connection_phase', 'N/A')}"
            )
            # Update the JSON field with the parsed dict to ensure it's saved as JSON
            lead.appliance_data = app_data
        
        lead.total_load_watts = total
        lead.save()

        # Auto-account creation logic
        if not lead.linked_user and lead.email:
            user_model = get_user_model()
            if not user_model.objects.filter(Q(email__iexact=lead.email) | Q(username__iexact=lead.email)).exists():
                username = lead.email.split('@')[0]
                base_username = username
                counter = 1
                while user_model.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                temp_pass = get_random_string(length=12)
                new_user = user_model.objects.create_user(
                    username=username, email=lead.email, password=temp_pass,
                    first_name=lead.name.split(' ')[0] if lead.name else "Solar",
                    last_name=" ".join(lead.name.split(' ')[1:]) if lead.name and ' ' in lead.name else "Customer",
                    phone=lead.phone
                )
                lead.linked_user = new_user
                lead.save()
                print(f"DEBUG: Auto-created user {username} for lead {lead.id}")


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrAdmin]


class StaffProfileViewSet(viewsets.ModelViewSet):
    queryset = StaffProfile.objects.all()
    serializer_class = StaffProfileSerializer
    permission_classes = [IsOwnerOrAdmin]

    def perform_create(self, serializer):
        email = self.request.data.get('email')
        staff = serializer.save()
        if email and not staff.user:
            user_model = get_user_model()
            if not user_model.objects.filter(email__iexact=email).exists():
                temp_pass = get_random_string(length=12)
                username = email.split('@')[0]
                base_username = username
                counter = 1
                while user_model.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                new_user = user_model.objects.create_user(
                    username=username, email=email, password=temp_pass,
                    first_name=staff.name.split(' ')[0], is_staff=True
                )
                staff.user = new_user
                staff.save()
                print(f"DEBUG: Created user {username} pass {temp_pass}")

    def perform_update(self, serializer):
        staff = serializer.save()
        if staff.status == StaffProfile.STATUS_TERMINATED:
            staff.is_active = False
            if staff.user:
                staff.user.is_active = False
                staff.user.save()
            staff.save()
        elif staff.status == StaffProfile.STATUS_ACTIVE:
            staff.is_active = True
            if staff.user:
                staff.user.is_active = True
                staff.user.save()
            staff.save()


class PayrollViewSet(viewsets.ModelViewSet):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [IsOwnerOrAdmin]

    @action(detail=True, methods=['get'])
    def download_slip(self, request, pk=None):
        from .payroll_views import generate_payroll_slip_pdf
        return generate_payroll_slip_pdf(request, pk)

    @action(detail=False, methods=['post'])
    def process_month(self, request):
        month_str = request.data.get('month')
        if not month_str:
            return Response({"error": "Month required"}, status=400)
        from datetime import datetime
        try:
            month_date = datetime.strptime(month_str, '%Y-%m-%d').date().replace(day=1)
        except:
            return Response({"error": "Invalid date"}, status=400)

        active_staff = StaffProfile.objects.filter(status=StaffProfile.STATUS_ACTIVE)
        created = 0
        for staff in active_staff:
            if not Payroll.objects.filter(staff=staff, month_year=month_date).exists():
                basic = staff.monthly_salary if staff.salary_type == StaffProfile.SALARY_MONTHLY else (staff.daily_wage * 26)
                commissions = Contact.objects.filter(
                    assigned_to=staff.user, lead_status=Contact.LEAD_WON,
                    created_at__month=month_date.month, created_at__year=month_date.year
                ).count() * staff.commission_per_lead if staff.user else 0
                Payroll.objects.create(
                    staff=staff, month_year=month_date, basic_salary=basic,
                    commissions=commissions, total_amount=basic + commissions
                )
                created += 1
        return Response({"message": f"Processed {created} records."}, status=201)
        

class ProjectFinancialsViewSet(viewsets.ModelViewSet):
    queryset = ProjectFinancials.objects.all()
    serializer_class = ProjectFinancialsSerializer
    permission_classes = [IsOwnerOrAdmin]

    @action(detail=True, methods=['get'])
    def download_report(self, request, pk=None):
        from .project_pdf_views import generate_project_report_pdf
        return generate_project_report_pdf(request, pk)


class JobPositionViewSet(viewsets.ModelViewSet):
    queryset = JobPosition.objects.all()
    serializer_class = JobPositionSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'list' and not is_owner_user(self.request.user):
            return qs.filter(is_active=True)
        return qs


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]


@login_required(login_url="/login/")
def admin_dashboard(request, path=''):
    if not is_owner_user(request.user):
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect("login")
    return render(request, "admin/dashboard.html")
