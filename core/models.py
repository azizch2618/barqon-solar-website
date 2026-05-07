from django.db import models
from django.utils import timezone
from django.conf import settings


class CompanyProfile(models.Model):
    company_name = models.CharField(max_length=200, default="BARQON Solar Solutions")
    owner_name = models.CharField(max_length=100, blank=True, default="Engr M Hassan")
    tagline = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    whatsapp = models.CharField(max_length=30, blank=True)
    website = models.URLField(blank=True)
    address = models.TextField(blank=True)
    logo = models.ImageField(upload_to="company/", blank=True, null=True)
    footer_note = models.TextField(
        blank=True,
        help_text="Footer text for quotations and public profile.",
    )
    bank_details = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def cleaned_whatsapp(self):
        if not self.whatsapp:
            return ""
        # Remove any non-digits
        clean = "".join(filter(str.isdigit, self.whatsapp))
        # If it starts with 0 (e.g. 0300...), replace with 92 (Pakistan)
        if clean.startswith("0") and len(clean) == 11:
            clean = "92" + clean[1:]
        return clean

    class Meta:
        verbose_name = "Company Profile"
        verbose_name_plural = "Company Profile"

    def __str__(self):
        return self.company_name


class Contact(models.Model):
    PROPERTY_HOME = "home"
    PROPERTY_SHOP = "shop"
    PROPERTY_HOTEL = "hotel"
    PROPERTY_RESTAURANT = "restaurant"
    PROPERTY_OFFICE = "office"
    PROPERTY_FACTORY = "factory"
    PROPERTY_OTHER = "other"

    PROPERTY_TYPE_CHOICES = [
        (PROPERTY_HOME, "Home"),
        (PROPERTY_SHOP, "Shop"),
        (PROPERTY_HOTEL, "Hotel"),
        (PROPERTY_RESTAURANT, "Restaurant"),
        (PROPERTY_OFFICE, "Office"),
        (PROPERTY_FACTORY, "Factory"),
        (PROPERTY_OTHER, "Other"),
    ]

    SYSTEM_HYBRID = "hybrid"
    SYSTEM_ON_GRID = "on_grid"
    SYSTEM_OFF_GRID = "off_grid"
    SYSTEM_NOT_SURE = "not_sure"

    SYSTEM_TYPE_CHOICES = [
        (SYSTEM_HYBRID, "Hybrid"),
        (SYSTEM_ON_GRID, "On Grid"),
        (SYSTEM_OFF_GRID, "Off Grid"),
        (SYSTEM_NOT_SURE, "Not Sure"),
    ]

    BATTERY_LITHIUM = "lithium"
    BATTERY_LEAD_ACID = "lead_acid"
    BATTERY_EITHER = "either"
    BATTERY_NO = "no_battery"

    BATTERY_PREFERENCE_CHOICES = [
        (BATTERY_LITHIUM, "Lithium"),
        (BATTERY_LEAD_ACID, "Lead Acid"),
        (BATTERY_EITHER, "Either"),
        (BATTERY_NO, "No Battery"),
    ]

    CONTACT_CALL = "call"
    CONTACT_WHATSAPP = "whatsapp"
    CONTACT_EMAIL = "email"

    CONTACT_METHOD_CHOICES = [
        (CONTACT_CALL, "Call"),
        (CONTACT_WHATSAPP, "WhatsApp"),
        (CONTACT_EMAIL, "Email"),
    ]

    LEAD_NEW = "new"
    LEAD_CONTACTED = "contacted"
    LEAD_QUOTED = "quoted"
    LEAD_WON = "won"
    LEAD_LOST = "lost"
    LEAD_CLOSED = "closed"

    LEAD_STATUS_CHOICES = [
        (LEAD_NEW, "New"),
        (LEAD_CONTACTED, "Contacted"),
        (LEAD_QUOTED, "Quoted"),
        (LEAD_WON, "Won"),
        (LEAD_LOST, "Lost"),
        (LEAD_CLOSED, "Closed"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=150, blank=True)
    message = models.TextField()
    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPE_CHOICES,
        default=PROPERTY_HOME,
    )
    city_area = models.CharField(max_length=150, blank=True)
    installation_address = models.TextField(blank=True)
    wapda_bill = models.FileField(upload_to="bills/", blank=True, null=True)
    wapda_bill_2 = models.FileField(upload_to="bills/", blank=True, null=True)
    wapda_bill_3 = models.FileField(upload_to="bills/", blank=True, null=True)
    system_type_preference = models.CharField(
        max_length=20,
        choices=SYSTEM_TYPE_CHOICES,
        default=SYSTEM_NOT_SURE,
    )
    monthly_bill = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    bill_month_1 = models.CharField(max_length=50, blank=True)
    bill_amount_1 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    bill_month_2 = models.CharField(max_length=50, blank=True)
    bill_amount_2 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    bill_month_3 = models.CharField(max_length=50, blank=True)
    bill_amount_3 = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fans = models.PositiveIntegerField(default=0)
    lights = models.PositiveIntegerField(default=0)
    ac = models.PositiveIntegerField(default=0)
    fridge = models.PositiveIntegerField(default=0)
    heater = models.PositiveIntegerField(default=0)
    iron = models.PositiveIntegerField(default=0)
    computers = models.PositiveIntegerField(default=0)
    motors = models.PositiveIntegerField(default=0)
    other_load_watts = models.PositiveIntegerField(default=0)
    total_load_watts = models.PositiveIntegerField(default=0, help_text="Calculated total peak load in Watts")
    appliance_data = models.JSONField(default=dict, blank=True, help_text="Structured appliance load JSON")
    load_details = models.TextField(blank=True)
    desired_backup_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    battery_preference = models.CharField(
        max_length=20,
        choices=BATTERY_PREFERENCE_CHOICES,
        default=BATTERY_EITHER,
    )
    wants_earth_bore = models.BooleanField(default=False)
    preferred_contact_method = models.CharField(
        max_length=20,
        choices=CONTACT_METHOD_CHOICES,
        default=CONTACT_CALL,
    )
    lead_status = models.CharField(
        max_length=20,
        choices=LEAD_STATUS_CHOICES,
        default=LEAD_NEW,
    )
    owner_notes = models.TextField(blank=True)
    is_resolved = models.BooleanField(default=False)
    is_viewed = models.BooleanField(default=False)
    linked_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customer_leads",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_leads",
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.phone}"


class Project(models.Model):
    STAGE_PENDING = "pending"
    STAGE_CIVIL = "civil_works"
    STAGE_ELECTRICAL = "electrical_works"
    STAGE_INSTALLATION = "panel_installation"
    STAGE_NET_METERING = "net_metering"
    STAGE_COMMISSIONING = "commissioning"
    STAGE_COMPLETED = "completed"
    STAGE_ON_HOLD = "on_hold"

    STAGE_CHOICES = [
        (STAGE_PENDING, "Pending / Survey"),
        (STAGE_CIVIL, "Civil Works"),
        (STAGE_ELECTRICAL, "Electrical Works"),
        (STAGE_INSTALLATION, "Panel Installation"),
        (STAGE_NET_METERING, "Net Metering"),
        (STAGE_COMMISSIONING, "Commissioning"),
        (STAGE_COMPLETED, "Completed"),
        (STAGE_ON_HOLD, "On Hold"),
    ]

    lead = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=STAGE_CHOICES, default=STAGE_PENDING)
    contract_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    assigned_engineer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_projects",
    )
    installation_date = models.DateField(null=True, blank=True)
    system_size_kw = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    location = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_paid(self):
        return sum(p.amount for p in self.payments.all())

    @property
    def balance_remaining(self):
        return self.contract_value - self.total_paid

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} – {self.get_status_display()}"


class ProjectPayment(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="payments"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True, help_text="Payment proof or details")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-payment_date", "-created_at"]

    def __str__(self):
        return f"Payment: {self.amount} for {self.project.title}"


class StaffProfile(models.Model):
    ROLE_ADMIN = "admin"
    ROLE_SALES = "sales"
    ROLE_ENGINEER = "engineer"
    ROLE_FABRICATOR = "fabricator"
    ROLE_LABOR = "labor"
    ROLE_HELPER = "helper"
    ROLE_ELECTRICIAN = "electrician"
    ROLE_INSTALLER = "installer"
    ROLE_OFFICE_BOY = "office_boy"

    ROLE_CHOICES = [
        (ROLE_ADMIN, "Admin"),
        (ROLE_SALES, "Sales"),
        (ROLE_ENGINEER, "Engineer"),
        (ROLE_FABRICATOR, "Fabricator"),
        (ROLE_LABOR, "Labor"),
        (ROLE_HELPER, "Helper"),
        (ROLE_ELECTRICIAN, "Electrician"),
        (ROLE_INSTALLER, "Installer"),
        (ROLE_OFFICE_BOY, "Office Boy"),
    ]

    STATUS_ACTIVE = 'active'
    STATUS_TERMINATED = 'terminated'
    STATUS_ON_LEAVE = 'on_leave'
    STATUS_RESIGNED = 'resigned'
    
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_TERMINATED, 'Terminated'),
        (STATUS_ON_LEAVE, 'On Leave'),
        (STATUS_RESIGNED, 'Resigned'),
    ]

    BANK_CHOICES = [
        ('hbl', 'Habib Bank Limited (HBL)'),
        ('ubl', 'United Bank Limited (UBL)'),
        ('mcb', 'MCB Bank Limited'),
        ('allied', 'Allied Bank Limited (ABL)'),
        ('meezan', 'Meezan Bank'),
        ('alfalah', 'Bank Alfalah'),
        ('standard_chartered', 'Standard Chartered'),
        ('askari', 'Askari Bank'),
        ('faysal', 'Faysal Bank'),
        ('bank_punjab', 'The Bank of Punjab (BOP)'),
        ('other', 'Other'),
    ]

    SALARY_MONTHLY = "monthly"
    SALARY_DAILY = "daily"

    SALARY_TYPE_CHOICES = [
        (SALARY_MONTHLY, "Monthly"),
        (SALARY_DAILY, "Daily Wages"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_profile",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    cnic = models.CharField(max_length=20, blank=True, verbose_name="CNIC / ID Number")
    address = models.TextField(blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_SALES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    
    # Salary Info
    salary_type = models.CharField(max_length=10, choices=SALARY_TYPE_CHOICES, default=SALARY_MONTHLY)
    monthly_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    daily_wage = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission_per_lead = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Commission earned per closed/won lead (PKR)",
    )
    
    # Bank Details
    bank_name = models.CharField(max_length=50, choices=BANK_CHOICES, blank=True)
    account_title = models.CharField(max_length=150, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    
    joined_date = models.DateField(null=True, blank=True)
    termination_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"


class Payroll(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PAID = 'paid'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PAID, 'Paid'),
    ]

    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='payrolls')
    month_year = models.DateField(help_text="Month and Year of the payroll (usually set to 1st of the month)")
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    commissions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    payment_date = models.DateField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-month_year"]
        unique_together = ["staff", "month_year"]

    def save(self, *args, **kwargs):
        self.total_amount = self.basic_salary + self.bonus + self.commissions - self.deductions
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payroll - {self.staff.name} - {self.month_year.strftime('%B %Y')}"


class SiteReview(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_location = models.CharField(max_length=100, blank=True)
    system_size = models.CharField(max_length=50, blank=True)
    rating = models.PositiveSmallIntegerField(default=5)
    review_text = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer_name} ({self.rating}/5)"


class SiteReviewPhoto(models.Model):
    review = models.ForeignKey(SiteReview, related_name='photos', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='reviews/')
    caption = models.CharField(max_length=200, blank=True)


class InstallationProject(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=100, blank=True)
    system_size = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class InstallationPhoto(models.Model):
    project = models.ForeignKey(InstallationProject, related_name='photos', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='installations/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]


class ProjectFinancials(models.Model):
    project = models.OneToOneField(
        Project, 
        on_delete=models.CASCADE, 
        related_name='financials',
        null=True, 
        blank=True
    )
    owner_name = models.CharField(max_length=200)
    details = models.TextField(blank=True)
    # items: [{"name": "...", "description": "...", "qty": 1, "cost": 100, "price": 150}, ...]
    items = models.JSONField(default=list) 
    
    total_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    profit_loss = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Project Financial"
        verbose_name_plural = "Project Financials"

    def save(self, *args, **kwargs):
        # Auto-calculate totals from items if provided
        cost = 0
        revenue = 0
        for item in self.items:
            try:
                qty = float(item.get('qty', 0))
                item_cost = float(item.get('cost', 0))
                item_price = float(item.get('price', 0))
                cost += (qty * item_cost)
                revenue += (qty * item_price)
            except (ValueError, TypeError):
                continue
        
        self.total_cost = cost
        self.total_revenue = revenue
        self.profit_loss = revenue - cost
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Financials: {self.owner_name} ({self.project.title if self.project else 'N/A'})"


class JobPosition(models.Model):
    JOB_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=100, default="Remote / Pakistan")
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default='full_time')
    description = models.TextField()
    requirements = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_job_type_display()})"


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('reviewing', 'Reviewing'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]
    position = models.ForeignKey(JobPosition, on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    experience_years = models.PositiveIntegerField(default=0)
    cover_letter = models.TextField(blank=True)
    cv = models.FileField(upload_to='cvs/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        pos_title = self.position.title if self.position else "General Application"
        return f"{self.full_name} - {pos_title}"
