from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class ServicePackage(models.Model):
    PACKAGE_TYPES = [
        ('basic', 'Basic Consulting'),
        ('premium', 'Premium Consulting'),
        ('vip', 'VIP Consulting'),
    ]
    
    name = models.CharField(max_length=100)
    package_type = models.CharField(max_length=10, choices=PACKAGE_TYPES)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    features = models.TextField(help_text="JSON list of features included")
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', 'price_usd']
    
    def __str__(self):
        return f"{self.name} - ${self.price_usd}"

class Order(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending Payment'),
        ('paid', 'Payment Confirmed'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    order_number = models.CharField(max_length=20, unique=True)
    package = models.ForeignKey(ServicePackage, on_delete=models.PROTECT)
    
    # Customer Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    
    # Academic Information
    current_education_level = models.CharField(max_length=100)
    desired_study_level = models.CharField(max_length=100)
    preferred_field = models.CharField(max_length=100)
    preferred_cities = models.CharField(max_length=200, blank=True)
    english_proficiency = models.CharField(max_length=50)
    
    # Order Details
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    order_status = models.CharField(max_length=15, choices=ORDER_STATUS, default='pending')
    payment_status = models.CharField(max_length=15, choices=PAYMENT_STATUS, default='pending')
    
    # Payment Information
    payment_method = models.CharField(max_length=50, blank=True)
    payment_id = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    
    # Additional Information
    special_requirements = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    assigned_consultant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.order_number} - {self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class OrderProgress(models.Model):
    PROGRESS_STAGES = [
        ('order_received', 'Order Received'),
        ('consultant_assigned', 'Consultant Assigned'),
        ('initial_consultation', 'Initial Consultation'),
        ('university_selection', 'University Selection'),
        ('application_preparation', 'Application Preparation'),
        ('applications_submitted', 'Applications Submitted'),
        ('admission_results', 'Admission Results'),
        ('visa_preparation', 'Visa Preparation'),
        ('visa_submitted', 'Visa Application Submitted'),
        ('visa_approved', 'Visa Approved'),
        ('pre_arrival_prep', 'Pre-arrival Preparation'),
        ('arrival_support', 'Arrival Support'),
        ('integration_complete', 'Integration Complete'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='progress')
    stage = models.CharField(max_length=25, choices=PROGRESS_STAGES)
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['order', 'stage']
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.order.order_number} - {self.get_stage_display()}"

class Testimonial(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    university = models.CharField(max_length=200)
    program = models.CharField(max_length=200)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    testimonial_text = models.TextField()
    photo = models.ImageField(upload_to='testimonials/', blank=True)
    is_featured = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.rating} stars"

