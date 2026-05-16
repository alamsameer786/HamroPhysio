# core/models.py - Complete error-free model code

from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.phone}"
    
    class Meta:
        ordering = ['-created_at']

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    SERVICE_CHOICES = [
        ('orthopaedic', 'Orthopaedic Rehab'),
        ('neurological', 'Neurological Rehab'),
        ('sports', 'Sports Injury'),
        ('post_surgery', 'Post-Surgery Recovery'),
        ('home_visit', 'Home Visit'),
        ('geriatric', 'Geriatric Care'),
    ]
    
    TIME_CHOICES = [
        ('09:00 AM - 10:00 AM', '09:00 AM - 10:00 AM'),
        ('10:00 AM - 11:00 AM', '10:00 AM - 11:00 AM'),
        ('11:00 AM - 12:00 PM', '11:00 AM - 12:00 PM'),
        ('12:00 PM - 01:00 PM', '12:00 PM - 01:00 PM'),
        ('02:00 PM - 03:00 PM', '02:00 PM - 03:00 PM'),
        ('03:00 PM - 04:00 PM', '03:00 PM - 04:00 PM'),
        ('04:00 PM - 05:00 PM', '04:00 PM - 05:00 PM'),
        ('05:00 PM - 06:00 PM', '05:00 PM - 06:00 PM'),
        ('06:00 PM - 07:00 PM', '06:00 PM - 07:00 PM'),
    ]
    
    booking_id = models.CharField(max_length=20, unique=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='bookings')
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    preferred_date = models.DateField()
    preferred_time = models.CharField(max_length=50, choices=TIME_CHOICES, blank=True, null=True)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=1800)
    discount_applied = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, default=1800)
    payment_mode = models.CharField(max_length=20, default='cod')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.booking_id:
            import random
            import string
            self.booking_id = 'HP' + ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.booking_id} - {self.patient.name}"
    
    class Meta:
        ordering = ['-preferred_date', '-created_at']

class Earning(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='earning')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default='pending')
    payment_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Earning for {self.booking.booking_id} - NPR {self.amount}"

class PartnershipRequest(models.Model):
    PARTNERSHIP_TYPES = [
        ('hospital', 'Hospital'),
        ('clinic', 'Clinic'),
        ('nursing_home', 'Nursing Home'),
        ('rehab_center', 'Rehabilitation Center'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('contacted', 'Contacted'),
        ('in_discussion', 'In Discussion'),
        ('partnered', 'Partnered'),
        ('declined', 'Declined'),
    ]
    
    request_id = models.CharField(max_length=20, unique=True, editable=False)
    organization_name = models.CharField(max_length=200)
    partnership_type = models.CharField(max_length=50, choices=PARTNERSHIP_TYPES)
    contact_person = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.request_id:
            import random
            import string
            self.request_id = 'PR' + ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.request_id} - {self.organization_name}"
    
    class Meta:
        ordering = ['-created_at']

class AdminLog(models.Model):
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.admin} - {self.action} - {self.timestamp}"

class Setting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.key} = {self.value}"