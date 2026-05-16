# core/decorators.py

from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    """Decorator to ensure user is admin/staff"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login first!')
            return redirect('admin_login')
        if not request.user.is_staff:
            messages.error(request, 'Access denied! Admin only.')
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return wrapper