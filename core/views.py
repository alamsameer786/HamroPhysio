from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Patient, Booking, Earning, PartnershipRequest, AdminLog
from .forms import PatientForm, BookingForm, AdminLoginForm, PartnershipRequestForm

def index(request):
    """Main website homepage"""
    return render(request, 'index.html', {'today': datetime.now()})

def book_appointment(request):
    """Book appointment page"""
    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        booking_form = BookingForm(request.POST)
        
        if patient_form.is_valid() and booking_form.is_valid():
            phone = patient_form.cleaned_data['phone']
            patient = Patient.objects.filter(phone=phone).first()
            
            if not patient:
                patient = patient_form.save()
            
            booking = booking_form.save(commit=False)
            booking.patient = patient
            booking.amount = 1800
            booking.discount_applied = 200
            booking.final_amount = 1600
            booking.payment_mode = 'cod'
            booking.status = 'pending'
            booking.save()
            
            Earning.objects.create(booking=booking, amount=booking.final_amount, payment_status='pending')
            
            messages.success(request, f'Booking confirmed! ID: {booking.booking_id}')
            return redirect('booking_success', booking_id=booking.booking_id)
    else:
        patient_form = PatientForm()
        booking_form = BookingForm()
    
    return render(request, 'book_appointment.html', {
        'patient_form': patient_form,
        'booking_form': booking_form,
    })

def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    return render(request, 'booking_success.html', {'booking': booking})

def admin_login(request):
    """Admin login page"""
    # If already logged in, redirect to dashboard
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            AdminLog.objects.create(admin=user, action='Admin logged in')
            messages.success(request, 'Welcome to Admin Dashboard!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'admin_login.html')

def admin_logout(request):
    """Admin logout"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('admin_login')

# IMPORTANT: Add @login_required decorator to protect these views
@login_required
def admin_dashboard(request):
    """Admin dashboard - REQUIRES LOGIN"""
    # Check if user is admin
    if not request.user.is_staff:
        messages.error(request, 'Access denied! Admin only.')
        return redirect('index')
    
    # Statistics
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    confirmed_bookings = Booking.objects.filter(status='confirmed').count()
    completed_bookings = Booking.objects.filter(status='completed').count()
    cancelled_bookings = Booking.objects.filter(status='cancelled').count()
    
    total_earnings = Earning.objects.filter(payment_status='received').aggregate(Sum('amount'))['amount__sum'] or 0
    pending_earnings = Earning.objects.filter(payment_status='pending').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expected = Booking.objects.aggregate(Sum('final_amount'))['final_amount__sum'] or 0
    
    # Recent bookings
    recent_bookings = Booking.objects.select_related('patient').all()[:10]
    
    # Service distribution
    service_stats = Booking.objects.values('service').annotate(
        count=Count('id'),
        total=Sum('final_amount')
    )
    
    context = {
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'completed_bookings': completed_bookings,
        'cancelled_bookings': cancelled_bookings,
        'total_earnings': total_earnings,
        'pending_earnings': pending_earnings,
        'total_expected': total_expected,
        'recent_bookings': recent_bookings,
        'service_stats': service_stats,
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def admin_bookings(request):
    """Manage bookings - REQUIRES LOGIN"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied! Admin only.')
        return redirect('index')
    
    bookings = Booking.objects.select_related('patient').all()
    
    # Filter by status
    status = request.GET.get('status', '')
    if status:
        bookings = bookings.filter(status=status)
    
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        action = request.POST.get('action')
        booking = get_object_or_404(Booking, id=booking_id)
        
        if action == 'confirm':
            booking.status = 'confirmed'
            booking.save()
            AdminLog.objects.create(admin=request.user, action=f'Confirmed booking {booking.booking_id}')
            messages.success(request, f'Booking {booking.booking_id} confirmed!')
        elif action == 'complete':
            booking.status = 'completed'
            booking.save()
            if hasattr(booking, 'earning'):
                booking.earning.payment_status = 'received'
                booking.earning.payment_date = timezone.now()
                booking.earning.save()
            AdminLog.objects.create(admin=request.user, action=f'Completed booking {booking.booking_id}')
            messages.success(request, f'Booking {booking.booking_id} completed!')
        elif action == 'cancel':
            booking.status = 'cancelled'
            booking.save()
            AdminLog.objects.create(admin=request.user, action=f'Cancelled booking {booking.booking_id}')
            messages.success(request, f'Booking {booking.booking_id} cancelled!')
        elif action == 'delete':
            booking.delete()
            AdminLog.objects.create(admin=request.user, action=f'Deleted booking {booking_id}')
            messages.success(request, 'Booking deleted!')
        
        return redirect('admin_bookings')
    
    context = {
        'bookings': bookings,
        'current_status': status,
    }
    return render(request, 'admin_bookings.html', context)

@login_required
def admin_patients(request):
    """Manage patients - REQUIRES LOGIN"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied! Admin only.')
        return redirect('index')
    
    patients = Patient.objects.all().prefetch_related('bookings')
    
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        if patient_id:
            patient = get_object_or_404(Patient, id=patient_id)
            patient.delete()
            AdminLog.objects.create(admin=request.user, action=f'Deleted patient {patient.name}')
            messages.success(request, 'Patient deleted!')
        return redirect('admin_patients')
    
    return render(request, 'admin_patients.html', {'patients': patients})

@login_required
def admin_earnings(request):
    """Earnings report - REQUIRES LOGIN"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied! Admin only.')
        return redirect('index')
    
    earnings = Earning.objects.select_related('booking__patient').all()
    
    # Filter by date range
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    if date_from:
        earnings = earnings.filter(payment_date__gte=date_from)
    if date_to:
        earnings = earnings.filter(payment_date__lte=date_to)
    
    total_received = earnings.filter(payment_status='received').aggregate(Sum('amount'))['amount__sum'] or 0
    total_pending = earnings.filter(payment_status='pending').aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'earnings': earnings,
        'total_received': total_received,
        'total_pending': total_pending,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'admin_earnings.html', context)

@login_required
def admin_settings(request):
    """Admin settings - REQUIRES LOGIN"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied! Admin only.')
        return redirect('index')
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password and new_password == confirm_password:
            user = request.user
            user.set_password(new_password)
            user.save()
            AdminLog.objects.create(admin=user, action='Changed password')
            messages.success(request, 'Password changed! Please login again.')
            logout(request)
            return redirect('admin_login')
        else:
            messages.error(request, 'Passwords do not match!')
    
    # Get admin logs
    logs = AdminLog.objects.select_related('admin').all()[:50]
    
    return render(request, 'admin_settings.html', {'logs': logs})

@login_required
def admin_partnerships(request):
    """Manage partnership requests - REQUIRES LOGIN"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied! Admin only.')
        return redirect('index')
    
    partnerships = PartnershipRequest.objects.all()
    
    # Filter by status
    status = request.GET.get('status', '')
    if status:
        partnerships = partnerships.filter(status=status)
    
    if request.method == 'POST':
        partnership_id = request.POST.get('partnership_id')
        action = request.POST.get('action')
        partnership = get_object_or_404(PartnershipRequest, id=partnership_id)
        
        if action == 'update_status':
            new_status = request.POST.get('status')
            partnership.status = new_status
            partnership.notes = request.POST.get('notes', '')
            partnership.save()
            AdminLog.objects.create(admin=request.user, action=f'Updated partnership {partnership.request_id} to {new_status}')
            messages.success(request, 'Partnership updated!')
        elif action == 'delete':
            partnership.delete()
            AdminLog.objects.create(admin=request.user, action=f'Deleted partnership {partnership.request_id}')
            messages.success(request, 'Partnership deleted!')
        
        return redirect('admin_partnerships')
    
    # Statistics
    total_requests = PartnershipRequest.objects.count()
    pending_requests = PartnershipRequest.objects.filter(status='pending').count()
    partnered_requests = PartnershipRequest.objects.filter(status='partnered').count()
    
    context = {
        'partnerships': partnerships,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'partnered_requests': partnered_requests,
        'current_status': status,
    }
    return render(request, 'admin_partnerships.html', context)

def partnership_request(request):
    """Partnership request form"""
    if request.method == 'POST':
        form = PartnershipRequestForm(request.POST)
        if form.is_valid():
            partnership = form.save()
            messages.success(request, f'Request submitted! ID: {partnership.request_id}')
            return redirect('partnership_success', request_id=partnership.request_id)
    else:
        form = PartnershipRequestForm()
    
    return render(request, 'partnership_form.html', {'form': form})

def partnership_success(request, request_id):
    partnership = get_object_or_404(PartnershipRequest, request_id=request_id)
    return render(request, 'partnership_success.html', {'partnership': partnership})

def custom_404(request, exception):
    """Custom 404 error page"""
    from django.http import HttpResponse
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head><title>Page Not Found - HamroPhysio</title></head>
    <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
        <h1>404 - Page Not Found</h1>
        <p>The page you're looking for doesn't exist.</p>
        <a href="/">Go back to Home</a>
    </body>
    </html>
    """, status=404)

def custom_500(request):
    """Custom 500 error page"""
    from django.http import HttpResponse
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head><title>Server Error - HamroPhysio</title></head>
    <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
        <h1>500 - Server Error</h1>
        <p>Something went wrong on our end. Please try again later.</p>
        <a href="/">Go back to Home</a>
    </body>
    </html>
    """, status=500)
