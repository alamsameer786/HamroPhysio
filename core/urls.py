from django.urls import path
from . import views

urlpatterns = [
    # Public URLs
    path('', views.index, name='index'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('booking-success/<str:booking_id>/', views.booking_success, name='booking_success'),
    path('partnership/', views.partnership_request, name='partnership_request'),
    path('partnership-success/<str:request_id>/', views.partnership_success, name='partnership_success'),
    
    # Admin URLs - Using YOUR underscore format
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_bookings/', views.admin_bookings, name='admin_bookings'),
    path('admin_patients/', views.admin_patients, name='admin_patients'),
    path('admin_earnings/', views.admin_earnings, name='admin_earnings'),
    path('admin_settings/', views.admin_settings, name='admin_settings'),
    path('admin_partnerships/', views.admin_partnerships, name='admin_partnerships'),
]