from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views

handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# Serve static and media files in production
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
