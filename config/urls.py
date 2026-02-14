"""
URL Configuration for MicroSaaS Concursos
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('modules/', include('modules.urls')),
    path('metrics/', include('metrics.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('user-management/', include('user_management.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "MicroSaaS Concursos - Administração"
admin.site.site_title = "Admin Concursos"
admin.site.index_title = "Painel Administrativo"
