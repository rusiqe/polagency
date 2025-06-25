from django.contrib import admin
from django.utils.html import format_html
from .models import ServicePackage, Order, OrderProgress, Testimonial
import json

@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'package_type', 'price_usd', 'is_active', 'is_featured', 'display_order']
    list_filter = ['package_type', 'is_active', 'is_featured']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'is_featured', 'display_order']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'package_type', 'price_usd')
        }),
        ('Content', {
            'fields': ('description', 'features')
        }),
        ('Settings', {
            'fields': ('is_active', 'is_featured', 'display_order')
        }),
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'get_full_name', 'email', 'package', 'total_amount', 'order_status', 'payment_status', 'created_at']
    list_filter = ['order_status', 'payment_status', 'package', 'created_at', 'assigned_consultant']
    search_fields = ['order_number', 'first_name', 'last_name', 'email']
    readonly_fields = ['order_number', 'created_at', 'updated_at', 'payment_date']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'package', 'total_amount', 'currency')
        }),
        ('Customer Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'country')
        }),
        ('Academic Information', {
            'fields': ('current_education_level', 'desired_study_level', 'preferred_field', 'preferred_cities', 'english_proficiency')
        }),
        ('Status', {
            'fields': ('order_status', 'payment_status', 'assigned_consultant')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_id', 'payment_date')
        }),
        ('Additional Information', {
            'fields': ('special_requirements', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('package', 'assigned_consultant')

@admin.register(OrderProgress)
class OrderProgressAdmin(admin.ModelAdmin):
    list_display = ['order', 'stage', 'completed', 'completed_date']
    list_filter = ['stage', 'completed', 'completed_date']
    search_fields = ['order__order_number', 'order__first_name', 'order__last_name']
    list_editable = ['completed']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'university', 'rating', 'is_featured', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_featured', 'is_approved', 'country', 'created_at']
    search_fields = ['name', 'university', 'program', 'testimonial_text']
    list_editable = ['is_featured', 'is_approved']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'country', 'photo')
        }),
        ('Academic Information', {
            'fields': ('university', 'program')
        }),
        ('Testimonial', {
            'fields': ('rating', 'testimonial_text')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_approved', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order')

