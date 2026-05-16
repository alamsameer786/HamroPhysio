# core/admin.py

from django.contrib import admin
from .models import Patient, Booking, Earning, AdminLog, Setting, PartnershipRequest

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'created_at']
    search_fields = ['name', 'phone']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'patient', 'service', 'preferred_date', 'status', 'final_amount']
    list_filter = ['status', 'service', 'preferred_date']
    search_fields = ['booking_id', 'patient__name', 'patient__phone']

@admin.register(Earning)
class EarningAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'payment_status', 'payment_date']

@admin.register(PartnershipRequest)
class PartnershipRequestAdmin(admin.ModelAdmin):
    list_display = ['request_id', 'organization_name', 'partnership_type', 'contact_person', 'status', 'created_at']
    list_filter = ['status', 'partnership_type']
    search_fields = ['request_id', 'organization_name', 'contact_person', 'email', 'phone']

@admin.register(AdminLog)
class AdminLogAdmin(admin.ModelAdmin):
    list_display = ['admin', 'action', 'timestamp']

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'value']