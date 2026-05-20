from rest_framework import serializers
from django.db import transaction

from .models import (
    CompanyProfile, Contact, Project, StaffProfile, Payroll,
    SiteReview, SiteReviewPhoto, InstallationProject, InstallationPhoto,
    ProjectFinancials, JobPosition, JobApplication, ProjectPayment, InventoryItem
)


class SiteReviewPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteReviewPhoto
        fields = ["id", "photo", "caption"]


class SiteReviewSerializer(serializers.ModelSerializer):
    photos = SiteReviewPhotoSerializer(many=True, read_only=True)
    uploaded_photos = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True, required=False
    )

    class Meta:
        model = SiteReview
        fields = [
            "id", "customer_name", "customer_location", "system_size",
            "rating", "review_text", "is_approved", "created_at", "photos", "uploaded_photos"
        ]
        read_only_fields = ["is_approved", "created_at"]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Please choose a rating from 1 to 5.")
        return value

    def create(self, validated_data):
        uploaded_photos = validated_data.pop('uploaded_photos', [])
        with transaction.atomic():
            review = SiteReview.objects.create(**validated_data)
            SiteReviewPhoto.objects.bulk_create(
                [SiteReviewPhoto(review=review, photo=photo) for photo in uploaded_photos]
            )
        return review


class InstallationPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallationPhoto
        fields = ["id", "photo", "caption", "order"]


class InstallationProjectSerializer(serializers.ModelSerializer):
    photos = InstallationPhotoSerializer(many=True, read_only=True)
    uploaded_photos = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True, required=False
    )

    class Meta:
        model = InstallationProject
        fields = [
            "id", "title", "location", "system_size", "description",
            "is_featured", "created_at", "photos", "uploaded_photos"
        ]

    def create(self, validated_data):
        uploaded_photos = validated_data.pop('uploaded_photos', [])
        with transaction.atomic():
            project = InstallationProject.objects.create(**validated_data)
            InstallationPhoto.objects.bulk_create(
                [
                    InstallationPhoto(project=project, photo=photo, order=i)
                    for i, photo in enumerate(uploaded_photos)
                ]
            )
        return project


class CompanyProfileSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = CompanyProfile
        fields = [
            "id",
            "company_name",
            "tagline",
            "email",
            "phone",
            "whatsapp",
            "website",
            "address",
            "logo",
            "logo_url",
            "footer_note",
            "bank_details",
            "updated_at",
        ]

    def get_logo_url(self, obj):
        request = self.context.get("request")
        if not obj.logo:
            return ""
        if request:
            return request.build_absolute_uri(obj.logo.url)
        return obj.logo.url


class ContactSerializer(serializers.ModelSerializer):
    wapda_bill_url = serializers.SerializerMethodField()
    wapda_bill_2_url = serializers.SerializerMethodField()
    wapda_bill_3_url = serializers.SerializerMethodField()
    assigned_to_username = serializers.CharField(source="assigned_to.username", read_only=True)
    lead_status_display = serializers.CharField(source="get_lead_status_display", read_only=True)
    property_type_display = serializers.CharField(source="get_property_type_display", read_only=True)

    class Meta:
        model = Contact
        fields = [
            "id", "name", "email", "phone", "subject", "message", "property_type",
            "city_area", "installation_address", "wapda_bill", "wapda_bill_2", "wapda_bill_3",
            "wapda_bill_url", "wapda_bill_2_url", "wapda_bill_3_url",
            "system_type_preference", "monthly_bill", "bill_month_1", "bill_amount_1",
            "bill_month_2", "bill_amount_2", "bill_month_3", "bill_amount_3",
            "fans", "lights", "ac", "fridge", "heater", "iron", "computers", "motors",
            "other_load_watts", "total_load_watts", "appliance_data", "load_details",
            "desired_backup_hours", "battery_preference", "wants_earth_bore",
            "preferred_contact_method", "lead_status", "assigned_to", "is_resolved", "is_viewed",
            "owner_notes", "created_at", "linked_user", "assigned_to_username",
            "lead_status_display", "property_type_display"
        ]
        read_only_fields = ["is_resolved", "created_at", "linked_user", "owner_notes"]

    def _get_file_url(self, file_field):
        request = self.context.get("request")
        if not file_field:
            return ""
        if request:
            return request.build_absolute_uri(file_field.url)
        return file_field.url

    def get_wapda_bill_url(self, obj):
        return self._get_file_url(obj.wapda_bill)

    def get_wapda_bill_2_url(self, obj):
        return self._get_file_url(obj.wapda_bill_2)

    def get_wapda_bill_3_url(self, obj):
        return self._get_file_url(obj.wapda_bill_3)


class ProjectSerializer(serializers.ModelSerializer):
    lead_name = serializers.CharField(source="lead.name", read_only=True)
    lead_phone = serializers.CharField(source="lead.phone", read_only=True)
    lead_city = serializers.CharField(source="lead.city_area", read_only=True)
    assigned_engineer_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    total_paid = serializers.DecimalField(source="annotated_total_paid", read_only=True, max_digits=12, decimal_places=2)
    balance_remaining = serializers.DecimalField(source="annotated_balance_remaining", read_only=True, max_digits=12, decimal_places=2)

    class Meta:
        model = Project
        fields = "__all__"

    def get_assigned_engineer_name(self, obj):
        if obj.assigned_engineer:
            return obj.assigned_engineer.get_full_name() or obj.assigned_engineer.username
        return ""


class ProjectPaymentSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source="project.title", read_only=True)

    class Meta:
        model = ProjectPayment
        fields = "__all__"


class StaffProfileSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source="get_role_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    bank_display = serializers.CharField(source="get_bank_name_display", read_only=True)
    salary_type_display = serializers.CharField(source="get_salary_type_display", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True, default="")

    class Meta:
        model = StaffProfile
        fields = "__all__"


class PayrollSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source="staff.name", read_only=True)
    staff_role = serializers.CharField(source="staff.get_role_display", read_only=True)
    month_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    
    # Aliases for frontend compatibility
    base_salary = serializers.DecimalField(source="basic_salary", max_digits=12, decimal_places=2, read_only=True)
    total_commission = serializers.DecimalField(source="commissions", max_digits=12, decimal_places=2, read_only=True)
    net_salary = serializers.DecimalField(source="total_amount", max_digits=12, decimal_places=2, read_only=True)
    month_display = serializers.SerializerMethodField()
    role_display = serializers.CharField(source="staff.get_role_display", read_only=True)

    class Meta:
        model = Payroll
        fields = "__all__"

    def get_month_name(self, obj):
        return obj.month_year.strftime('%B %Y')

    def get_month_display(self, obj):
        return obj.month_year.strftime('%B %Y')


class ProjectFinancialsSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source="project.title", read_only=True)
    
    class Meta:
        model = ProjectFinancials
        fields = "__all__"


class JobPositionSerializer(serializers.ModelSerializer):
    job_type_display = serializers.CharField(source="get_job_type_display", read_only=True)
    applications_count = serializers.IntegerField(source="applications.count", read_only=True)

    class Meta:
        model = JobPosition
        fields = "__all__"


class InventoryItemSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = InventoryItem
        fields = [
            "id", "name", "sku", "category", "category_display",
            "quantity_on_hand", "reorder_level", "unit_cost",
            "supplier", "notes", "is_low_stock", "created_at", "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at", "is_low_stock"]


class JobApplicationSerializer(serializers.ModelSerializer):
    position_title = serializers.SerializerMethodField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    cv_url = serializers.SerializerMethodField()

    class Meta:
        model = JobApplication
        fields = "__all__"

    def get_position_title(self, obj):
        return obj.position.title if obj.position else "General Application"

    def get_cv_url(self, obj):
        request = self.context.get("request")
        if not obj.cv:
            return ""
        if request:
            return request.build_absolute_uri(obj.cv.url)
        return obj.cv.url
