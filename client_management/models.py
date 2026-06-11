from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image

from core.models import BaseModel

def validate_png(image):
    if not image.name.lower().endswith('.png'):
        raise ValidationError("Only PNG images are allowed.")

def validate_image_dimensions(image):
    img = Image.open(image)
    width, height = img.size

    if width != 300 or height != 300:
        raise ValidationError("Image must be exactly 300x300 pixels.")
    
    
class Client(BaseModel):
    company_name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    gst_number = models.CharField(max_length=100, blank=True, null=True)
    country = models.ForeignKey('master.Country', on_delete=models.SET_NULL, blank=True, null=True)
    state = models.ForeignKey('master.State', on_delete=models.SET_NULL, blank=True, null=True)
    district = models.ForeignKey('master.District', on_delete=models.SET_NULL, blank=True, null=True)
    area = models.ForeignKey('master.Area', on_delete=models.SET_NULL, blank=True, null=True)

    business_name = models.CharField(max_length=200, blank=True, null=True)
    licenses_count = models.IntegerField(blank=True, null=True)
    max_branches = models.IntegerField(blank=True, null=True)
    monthly_tariff = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # next_renewal_date = models.DateField(blank=True, null=True)

    scheme_types = models.ManyToManyField('master.SchemeType', blank=True)
    
    logo_color = models.ImageField(
        upload_to='client_logos/color/',
        validators=[validate_png, validate_image_dimensions],
        blank=True,
        null=True
    )

    logo_bw = models.ImageField(
        upload_to='client_logos/bw/',
        validators=[validate_png, validate_image_dimensions],
        blank=True,
        null=True
    )
    
    def __str__(self):
        return f"{self.company_name} ({self.owner_name})"


class Subscription(BaseModel):
    company = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateField()
    end_date = models.DateField()
    usage_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    no_of_licenses = models.PositiveIntegerField(default=1)

    # Feature flags
    whatsapp_integration = models.BooleanField(default=False)
    bulk_sms = models.BooleanField(default=False)
    email_integration = models.BooleanField(default=False)
    bluetooth_printing = models.BooleanField(default=False)
    tally_integration = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company.company_name} ({self.start_date} → {self.end_date})"

    @property
    def is_active(self):
        from django.utils import timezone
        return self.start_date <= timezone.now().date() <= self.end_date


class SubscriptionNotification(models.Model):
    subscription = models.ForeignKey(
        'Subscription',
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.TextField()
    notify_date = models.DateField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.message
    
    
from django.contrib.auth.models import User

class Branch(BaseModel):
    company = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    gst_number = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='branch_logos/', blank=True, null=True)
    branch_admin = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_branch')

    scheme_types = models.ManyToManyField('master.SchemeType', blank=True)
    invoice_prefix = models.CharField(
        max_length=5, blank=True, null=True,
        help_text="Letter prefix for invoices (e.g. A → INV-A-1). Leave blank to auto-assign."
    )
    
    def __str__(self):
        return f"{self.name} - {self.company.company_name}"

class Staff(BaseModel):
    DESIGNATION_CHOICES = (
        ('BRANCH_MANAGER', 'Branch manager'),
        ('MARKETING', 'Marketing'),
        ('CLERICAL', 'Clerical'),
        ('SERVICE', 'Service'),
    )

    SALARY_MODE_SALARIED = 'SALARIED'
    SALARY_MODE_WAGE = 'WAGE'
    SALARY_MODE_COMMISSION = 'COMMISSION'
    SALARY_MODE_CHOICES = (
        (SALARY_MODE_SALARIED, 'Salaried'),
        (SALARY_MODE_WAGE, 'Wage'),
        (SALARY_MODE_COMMISSION, 'Commissioned'),
    )

    company = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='staffs')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='staffs')
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)
    name = models.CharField(max_length=200)
    employee_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='staff_profile')

    # Salary
    salary_mode = models.CharField(
        max_length=20,
        choices=SALARY_MODE_CHOICES,
        default=SALARY_MODE_SALARIED
    )
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                          help_text='Applicable when Salary Mode is Salaried')
    daily_wage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                      help_text='Applicable when Salary Mode is Wage')

    def __str__(self):
        return f"{self.name} ({self.employee_id}) - {self.get_designation_display()}"


class StaffCommission(BaseModel):
    """Commission configuration for a commissioned staff member per service + vehicle type."""
    COMMISSION_TYPE_PERCENTAGE = 'PERCENTAGE'
    COMMISSION_TYPE_EXACT = 'EXACT'
    COMMISSION_TYPE_CHOICES = (
        (COMMISSION_TYPE_PERCENTAGE, 'Percentage (%)'),
        (COMMISSION_TYPE_EXACT, 'Exact Amount (₹)'),
    )

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='commissions')
    service = models.ForeignKey('service_management.Service', on_delete=models.CASCADE, related_name='staff_commissions')
    vehicle_type = models.ForeignKey('master.VehicleType', on_delete=models.CASCADE, related_name='staff_commissions')
    commission_type = models.CharField(max_length=20, choices=COMMISSION_TYPE_CHOICES, default=COMMISSION_TYPE_PERCENTAGE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Percentage or exact amount depending on commission_type')

    class Meta:
        unique_together = ('staff', 'service', 'vehicle_type')

    def __str__(self):
        return f"{self.staff.name} | {self.service.name} | {self.vehicle_type.name} → {self.amount}"


class CustomerType(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'customer_type'
        ordering = ['-id']

class Customer(BaseModel):
    company = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='customers')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='customers')
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    customer_type = models.ForeignKey(CustomerType, on_delete=models.SET_NULL, null=True, blank=False)
    whatsapp_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    pincode = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"

class CustomerVehicle(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='vehicles')
    vehicle_type = models.ForeignKey('master.VehicleType', on_delete=models.CASCADE, blank=True, null=True)
    vehicle_type_model = models.ForeignKey('master.VehicleTypeModel', on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.vehicle_number} - {self.vehicle_type_model.name}"


class Scheme(BaseModel):
    SCHEME_BENEFIT_QTY = 'Quantity'
    SCHEME_BENEFIT_DISCOUNT = 'Discount'
    SCHEME_BENEFIT_VOUCHER = 'Voucher'

    company = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='schemes')
    scheme_type = models.ForeignKey('master.SchemeType', on_delete=models.CASCADE, related_name='schemes')
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

    services = models.ManyToManyField('service_management.Service', blank=True, related_name='schemes')
    customer_types = models.ManyToManyField(CustomerType, blank=True, related_name='schemes')
    vehicle_types = models.ManyToManyField('master.VehicleType', blank=True, related_name='schemes')

    # Quantity benefit
    paid_visits = models.IntegerField(null=True, blank=True)
    free_visits = models.IntegerField(null=True, blank=True)

    # Discount benefit
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_added']


class SchemeVoucher(BaseModel):
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, related_name='vouchers')
    voucher_number = models.CharField(max_length=100)
    discount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.scheme.name} - {self.voucher_number}"


class ComplaintType(BaseModel):
    company = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='complaint_types')
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} ({self.company.company_name})"


class Complaint(BaseModel):
    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_HIGH, 'High'),
    ]

    STATUS_NEW = 'new'
    STATUS_PENDING = 'pending'
    STATUS_RESOLVED = 'resolved'
    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_PENDING, 'Pending'),
        (STATUS_RESOLVED, 'Resolved'),
    ]

    company = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='complaints')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='complaints')
    complaint_type = models.ForeignKey(ComplaintType, on_delete=models.CASCADE, related_name='complaints')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default=PRIORITY_LOW)
    complaint_description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    resolve_remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Complaint #{self.auto_id} - {self.branch.name} ({self.status})"


class WhatsAppSetting(BaseModel):
    company = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='whatsapp_setting')
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    whatsapp_number = models.CharField(max_length=30)

    def __str__(self):
        return f"WhatsApp Setting - {self.company.company_name}"


class WhatsAppTemplate(BaseModel):
    company = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='whatsapp_templates')
    template_name = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return f"{self.template_name} - {self.company.company_name}"


class Stock(BaseModel):
    UNIT_CHOICES = (
        ('Litre', 'Litre (Ltr)'),
        ('Millilitre', 'Millilitre (ml)'),
        ('Kilogram', 'Kilogram (Kg)'),
        ('Gram', 'Gram (g)'),
        ('Piece', 'Piece (Pcs)'),
        ('Box', 'Box'),
        ('Packet', 'Packet'),
        ('Bottle', 'Bottle'),
        ('Can', 'Can'),
        ('Roll', 'Roll'),
    )

    company = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='stocks', null=True, blank=True)
    item_name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES)

    def __str__(self):
        if self.company:
            return f"{self.item_name} ({self.get_unit_display()}) - {self.company.company_name}"
        return f"{self.item_name} ({self.get_unit_display()}) - Global"


class StaffLeave(BaseModel):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='leaves')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPROVED')

    def __str__(self):
        return f"{self.staff.name} ({self.start_date} to {self.end_date})"


class PurchaseRequest(BaseModel):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    company = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='purchase_requests')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='purchase_requests', null=True, blank=True)
    date = models.DateField()
    material = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='purchase_requests')
    qty = models.DecimalField(max_digits=10, decimal_places=2)
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.material.item_name} - {self.qty} ({self.date})"


class Extra(BaseModel):
    company = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='extras', null=True, blank=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        if self.company:
            return f"{self.name} - {self.company.company_name}"
        return self.name