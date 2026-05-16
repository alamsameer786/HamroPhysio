# core/forms.py - Complete error-free form code

from django import forms
from .models import Patient, Booking, PartnershipRequest

# Time choices for dropdown
TIME_CHOICES = [
    ('', '-- Select Preferred Time --'),
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

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'phone', 'email', 'address']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-3 border rounded-xl focus:ring-2 focus:ring-[#C68E17] focus:border-transparent',
                'placeholder': 'Full Name',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full p-3 border rounded-xl focus:ring-2 focus:ring-[#C68E17] focus:border-transparent',
                'placeholder': 'Phone Number',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-3 border rounded-xl focus:ring-2 focus:ring-[#C68E17] focus:border-transparent',
                'placeholder': 'Email (optional)'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full p-3 border rounded-xl focus:ring-2 focus:ring-[#C68E17] focus:border-transparent',
                'placeholder': 'Your Address',
                'rows': 3,
                'required': True
            }),
        }

class BookingForm(forms.ModelForm):
    preferred_time = forms.ChoiceField(
        choices=TIME_CHOICES, 
        required=True,
        widget=forms.Select(attrs={
            'class': 'w-full p-3 border rounded-xl focus:ring-2 focus:ring-[#C68E17] focus:border-transparent'
        })
    )
    
    class Meta:
        model = Booking
        fields = ['service', 'preferred_date', 'preferred_time', 'address', 'notes']
        widgets = {
            'service': forms.Select(attrs={
                'class': 'w-full p-3 border rounded-xl focus:ring-2 focus:ring-[#C68E17] focus:border-transparent'
            }),
            'preferred_date': forms.DateInput(attrs={
                'class': 'w-full p-3 border rounded-xl focus:ring-2 focus:ring-[#C68E17] focus:border-transparent',
                'type': 'date',
                'min': '2025-01-01'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full p-3 border rounded-xl focus:ring-2 focus:ring-[#C68E17] focus:border-transparent',
                'rows': 3,
                'placeholder': 'Full address for home visit'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full p-3 border rounded-xl focus:ring-2 focus:ring-[#C68E17] focus:border-transparent',
                'rows': 2,
                'placeholder': 'Any specific instructions or symptoms?'
            }),
        }

class AdminLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-3 border rounded-xl focus:ring-2 focus:ring-[#C68E17] focus:border-transparent',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full p-3 border rounded-xl focus:ring-2 focus:ring-[#C68E17] focus:border-transparent',
        'placeholder': 'Password'
    }))

class PartnershipRequestForm(forms.ModelForm):
    class Meta:
        model = PartnershipRequest
        fields = ['organization_name', 'partnership_type', 'contact_person', 'email', 'phone', 'address', 'message']
        widgets = {
            'organization_name': forms.TextInput(attrs={
                'class': 'w-full p-3 border rounded-xl focus:ring-2 focus:ring-[#C68E17] focus:border-transparent',
                'placeholder': 'Hospital/Clinic Name'
            }),
            'partnership_type': forms.Select(attrs={
                'class': 'w-full p-3 border rounded-xl focus:ring-2 focus:ring-[#C68E17] focus:border-transparent'
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'w-full p-3 border rounded-xl focus:ring-2 focus:ring-[#C68E17] focus:border-transparent',
                'placeholder': 'Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-3 border rounded-xl focus:ring-2 focus:ring-[#C68E17] focus:border-transparent',
                'placeholder': 'Email Address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full p-3 border rounded-xl focus:ring-2 focus:ring-[#C68E17] focus:border-transparent',
                'placeholder': 'Phone Number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full p-3 border rounded-xl focus:ring-2 focus:ring-[#C68E17] focus:border-transparent',
                'placeholder': 'Complete Address',
                'rows': 3
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full p-3 border rounded-xl focus:ring-2 focus:ring-[#C68E17] focus:border-transparent',
                'placeholder': 'Tell us about your organization and how we can collaborate...',
                'rows': 4
            }),
        }